# novatube

`novatube` is a Telegram bot designed to download videos from various content platforms such as YouTube and Reddit, and deliver them directly to users through Telegram.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed the latest version of [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/).
- You have a Telegram bot token from BotFather.

## Installation

To install VideoDownloaderBot, follow these steps:

1. Clone the repository to your local machine:
```bash
git clone https://github.com/totekuh/novatube.git
cd novatube
```

Create a `.env` file inside the devops directory based on the `docker.env.example` template:

```bash
cp devops/docker.env.example devops/docker.env
```

Then, edit `devops/docker.env` to include your specific configurations such as the Telegram bot token.

Run the application using the provided script:

```bash
./run.sh
```

## Usage

After installation, interact with the Telegram bot using the following commands:

- `/start` - Welcome message and usage instructions.
- `/help` - Show help information.
- `/youtube` - Download a video from YouTube by providing a URL.
- `/reddit` - Download a video from Reddit by providing a URL.

