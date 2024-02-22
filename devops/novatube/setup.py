#!/usr/bin/env python3

version = "1.0.0"

from setuptools import setup, find_packages

setup(
    name="novatube",
    version=version,
    description="A Python telegram bot for downloading videos from YouTube and Reddit",
    long_description_content_type='text/markdown',  # Add this line
    author="totekuh",
    author_email="totekuh@protonmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "novatube=novatube.novatube_runner:main",
        ],
    },
    url='https://github.com/totekuh/novatube',  # Optional
    install_requires=[
        "telebot",
        "yt-dlp"
    ],
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/totekuh/novatube/issues',
        'Source': 'https://github.com/totekuh/novatube',
    },

)
