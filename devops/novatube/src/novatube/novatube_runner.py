#!/usr/bin/env python3
import telebot
import os
import sys
import re
import logging
import subprocess
from uuid import uuid4
import glob

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("Bot token can not be empty")
ALLOWED_USERS = [user.strip() for user in os.getenv("ALLOWED_USERS").split(",")]


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(BOT_TOKEN)
user_urls = {}  # Dictionary to temporarily store URLs provided by users


SOURCE_YOUTUBE = "YouTube"
SOURCE_REDDIT = "Reddit"


def is_valid_youtube_url(url):
    """Simple validation for YouTube URLs."""
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    youtube_regex_match = re.match(youtube_regex, url)
    return bool(youtube_regex_match)


def send_welcome(message):
    help_message = (
        "Welcome to VideoDownloaderBot! Here's how you can use this bot:\n\n"
        "/youtube - Download a video from YouTube.\n"
        "/reddit - Download a video from Reddit.\n\n"
        "Just send the command followed by the video URL!"
    )
    bot.reply_to(message, help_message)


def ask_for_youtube_url(message):
    bot.send_message(message.chat.id, 'Please paste the YouTube video URL:')
    bot.register_next_step_handler(message, process_youtube_url)


def process_youtube_url(message):
    chat_id = message.chat.id
    url = message.text
    if not is_valid_youtube_url(url):
        bot.send_message(chat_id, "This does not appear to be a valid YouTube URL. Please try again.")
        return
    download_video(chat_id, url, source=SOURCE_YOUTUBE)


def get_youtube_resolutions(url):
    command = ['yt-dlp', '-F', url]
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if process.returncode != 0:
        logger.error(f"Error retrieving information from YouTube: {process.stderr}")
        return None

    # Parse the command output using regex to find resolution information
    video_lines = re.findall(r'^\d+\s+mp4\s+(\d+x\d+)\s+\d+', process.stdout, re.MULTILINE)
    resolutions = sorted(set([re.sub(r'x\d+', '', res) for res in video_lines]), key=int, reverse=True)
    return resolutions


def download_video(chat_id, url, source="Website", resolution='360p'):
    base_filename = str(uuid4())  # Generate a unique identifier for the filename
    temp_output_pattern = f"{base_filename}*"  # Pattern to match the downloaded file
    output_file = ""

    try:
        bot.send_message(chat_id, f"Starting download from {source}. This may take a while...")

        # Download with yt-dlp without specifying an extension
        if resolution.endswith("p"):
            resolution = resolution[:-1]

        if source == SOURCE_YOUTUBE:
            yt_dlp_command = ['yt-dlp', '-f', f'best[height<={resolution}]', url, '-o', base_filename]
        elif source == SOURCE_REDDIT:
            yt_dlp_command = ['yt-dlp', url, '-o', base_filename]
        else:
            raise Exception(f"Unknown source: {source}")

        subprocess.run(yt_dlp_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        # Find the downloaded file with glob
        downloaded_files = glob.glob(temp_output_pattern)
        if not downloaded_files:
            bot.send_message(chat_id, "No video file was downloaded.")
            return
        else:
            bot.send_message(chat_id, "Video was downloaded, uploading it now...")
            output_file = downloaded_files[0]
            with open(output_file, 'rb') as video:
                bot.send_video(chat_id, video, timeout=360)
            os.remove(output_file)

    except Exception as e:
        logger.error(f"Error downloading from {source}: {e}")
        bot.send_message(chat_id, f"Failed to download the video from {source}. Please try again.")
        # Clean up any remaining files in case of failure
        for file in glob.glob(temp_output_pattern):
            os.remove(file)
        if os.path.exists(output_file):
            os.remove(output_file)


def ask_for_reddit_url(message):
    bot.send_message(message.chat.id, 'Please paste the Reddit post URL:')
    bot.register_next_step_handler(message, process_reddit_url)


def process_reddit_url(message):
    chat_id = message.chat.id
    url = message.text
    if "reddit.com" not in url:
        bot.send_message(chat_id, "This does not appear to be a valid Reddit URL. Please try again.")
        return
    # Store URL and proceed to download
    user_urls[chat_id] = url
    download_video(chat_id, url, source=SOURCE_REDDIT)

def is_user_allowed(username):
    return username in ALLOWED_USERS

@bot.message_handler(commands=['youtube', 'reddit', 'start', 'help'])
def handle_commands(message):
    username = message.from_user.username
    if not is_user_allowed(username):
        bot.reply_to(message, "You are not authorized to use this bot.")
        return

    # Continue with the command if the user is allowed
    if message.text.startswith('/youtube'):
        ask_for_youtube_url(message)
    elif message.text.startswith('/reddit'):
        ask_for_reddit_url(message)
    elif message.text in ['/start', '/help']:
        send_welcome(message)
    else:
        bot.reply_to(message, "Command not recognized.")


def main():
    try:
        bot.polling(non_stop=True)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error polling: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
