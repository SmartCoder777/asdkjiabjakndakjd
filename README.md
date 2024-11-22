# Telegram DRM Bot

A Telegram bot that downloads encrypted video/audio files using `N_m3u8DL-CLI`, decrypts them using `mp4decrypt`, merges them using `ffmpeg`, and sends the final file to the user.

## Features
- Download encrypted video and audio files.
- Decrypt the files with provided DRM keys.
- Merge video and audio files.
- Send the processed file back to the user.

## Prerequisites
- Python 3.8 or higher
- Telegram Bot Token (create one using [BotFather](https://t.me/BotFather))
- Executables: `N_m3u8DL-CLI`, `mp4decrypt`, and `ffmpeg`.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/telegram-drm-bot.git
   cd telegram-drm-bot
