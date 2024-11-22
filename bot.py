import os
from pyrogram import Client, filters
import subprocess

# Initialize the bot
api_id = "13794728"
api_hash = "25c1a5b45b981d601832905e220e16c7"
bot_token = "7691929412:AAHtLk2-e_gVKfhN-9KHWZAxYv7m9_RT_8w"

bot = Client("drm_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Store user-specific data temporarily
user_data = {}

@bot.on_message(filters.command("link"))
async def ask_for_url(client, message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    await message.reply("Please send the URL.")
    user_data[chat_id]['step'] = 'url'

@bot.on_message(filters.text & ~filters.command)
async def collect_data(client, message):
    chat_id = message.chat.id
    if chat_id not in user_data or 'step' not in user_data[chat_id]:
        return

    step = user_data[chat_id]['step']

    if step == 'url':
        user_data[chat_id]['url'] = message.text
        await message.reply("Please send the DRM key for the video.")
        user_data[chat_id]['step'] = 'video_key'

    elif step == 'video_key':
        user_data[chat_id]['video_key'] = message.text
        await message.reply("Please send the DRM key for the audio.")
        user_data[chat_id]['step'] = 'audio_key'

    elif step == 'audio_key':
        user_data[chat_id]['audio_key'] = message.text
        await message.reply("Please provide a name for the output file (without extension).")
        user_data[chat_id]['step'] = 'file_name'

    elif step == 'file_name':
        user_data[chat_id]['file_name'] = message.text
        await message.reply("Processing your request...")
        await process_request(client, chat_id)

async def process_request(client, chat_id):
    try:
        # Extract user inputs
        url = user_data[chat_id]['url']
        video_key = user_data[chat_id]['video_key']
        audio_key = user_data[chat_id]['audio_key']
        file_name = user_data[chat_id]['file_name']

        # Define file paths
        download_dir = "./downloads"
        video_file = os.path.join(download_dir, "video.mp4")
        audio_file = os.path.join(download_dir, "audio.aac")
        decrypted_video = os.path.join(download_dir, "decrypted_video.mp4")
        decrypted_audio = os.path.join(download_dir, "decrypted_audio.aac")
        final_file = os.path.join(download_dir, f"{file_name}.mp4")

        os.makedirs(download_dir, exist_ok=True)

        # Step 1: Download video and audio
        subprocess.run([
            "N_m3u8DL-CLI_v3.0.2.exe",
            url,
            "--workDir", download_dir
        ], check=True)

        # Step 2: Decrypt video and audio
        subprocess.run([
            "mp4decrypt.exe",
            "--key", f"1:{video_key}",
            video_file,
            decrypted_video
        ], check=True)

        subprocess.run([
            "mp4decrypt.exe",
            "--key", f"1:{audio_key}",
            audio_file,
            decrypted_audio
        ], check=True)

        # Step 3: Merge video and audio
        subprocess.run([
            "ffmpeg.exe",
            "-i", decrypted_video,
            "-i", decrypted_audio,
            "-c", "copy",
            final_file
        ], check=True)

        # Step 4: Send the file back to the user
        await client.send_document(chat_id, final_file)
        await client.send_message(chat_id, "Here is your processed file!")

    except Exception as e:
        await client.send_message(chat_id, f"An error occurred: {str(e)}")

    finally:
        # Clean up
        if os.path.exists(download_dir):
            for f in os.listdir(download_dir):
                os.remove(os.path.join(download_dir, f))
            os.rmdir(download_dir)
        user_data.pop(chat_id, None)

if __name__ == "__main__":
    bot.run()
