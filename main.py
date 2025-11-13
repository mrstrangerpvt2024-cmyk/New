import os
import re
import sys
import time
import asyncio
import requests
import subprocess
from subprocess import getstatusoutput
from aiohttp import ClientSession

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyromod import listen

import helper
from logger import logging
from vars import API_ID, API_HASH, BOT_TOKEN

# --- Bot Init ---
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

photo = "youtube.jpg"
start_ph = "image-optimisation-scaled.jpg"
api_url = "http://master-api-v3.vercel.app/"
api_token = "YOUR_API_TOKEN_HERE"
token_cp = "YOUR_CP_TOKEN_HERE"
CR = "S A K S H A M"

# -------------------- CAPTION TEMPLATES --------------------
def get_captions(file_type, count, name1, res, b_name, url=None):
    count_str = str(count).zfill(3)
    if file_type in ["mkv", "mp4"]:
        return f'╭━━━━━━━━━━━╮\n**🎥 VIDEO ID :** {count_str}\n╰━━━━━━━━━━━╯\n\n**📄 Title : {name1}** ({res}) ᴍʀꜱᴛʀᴀɴɢᴇʀ™.{file_type}\n\n**🔗 Video Url :** <a href="{url}">__Click Here to Watch Video__</a>\n\n**🔖 Batch :** `{b_name}`\n**📥 Extracted By :** {CR}' if url else f'╭━━━━━━━━━━━╮\n**🎥 VIDEO ID :** {count_str}\n╰━━━━━━━━━━━╯\n\n**📄 Title : {name1}** ({res}) ᴍʀꜱᴛʀᴀɴɢᴇʀ™.{file_type}\n\n**🔖 Batch :** `{b_name}`\n**📥 Extracted By :** {CR}'
    elif file_type == "pdf":
        return f'╭━━━━━━━━━━━╮\n**📁 FILE ID :** {count_str}\n╰━━━━━━━━━━━╯\n\n**📄 Title : {name1}** ᴍʀꜱᴛʀᴀɴɢᴇʀ™.pdf\n\n**🔖 Batch :** `{b_name}`\n**📥 Extracted By :** {CR}'
    elif file_type == "zip":
        return f'╭━━━━━━━━━━━╮\n**📁 FILE ID :** {count_str}\n╰━━━━━━━━━━━╯\n\n**📄 Title : {name1}** ᴍʀꜱᴛʀᴀɴɢᴇʀ™.zip\n\n**🔖 Batch :** `{b_name}`\n**📥 Extracted By :** {CR}'
    elif file_type == "jpg":
        return f'╭━━━━━━━━━━━╮\n**🖼️ IMAGE ID :** {count_str}\n╰━━━━━━━━━━━╯\n\n**📄 Title : {name1}** ᴍʀꜱᴛʀᴀɴɢᴇʀ™.jpg\n\n**🔖 Batch :** `{b_name}`\n**📥 Extracted By :** {CR}'
    elif file_type == "mp3":
        return f'╭━━━━━━━━━━━╮\n**🎵 AUDIO ID :** {count_str}\n╰━━━━━━━━━━━╯\n\n**📄 Title : {name1}** ({res}) ᴍʀꜱᴛʀᴀɴɢᴇʀ™.mp3\n\n**🔖 Batch :** `{b_name}`\n**📥 Extracted By :** {CR}'
    elif file_type == "html":
        return f'╭━━━━━━━━━━━╮\n**🌐 HTML ID :** {count_str}\n╰━━━━━━━━━━━╯\n\n**📄 Title : {name1}** ({res}) ᴍʀꜱᴛʀᴀɴɢᴇʀ™.html\n\n**🔖 Batch :** `{b_name}`\n**📥 Extracted By :** {CR}'
    return ""

# -------------------- BOT COMMANDS --------------------
@bot.on_message(filters.command("start"))
async def start(bot, m: Message):
    welcome_text = (
        "📦 **TXT File Downloader Bot**\n\n"
        "👋 **I’m your one and only TXT File Downloader Bot**\n"
        "📌 **What I Can Do:** Clean TXT downloads | Fast | User-Friendly\n"
        "🚀 **How To Use:** Send `/txt` to start\n"
        "🔥 **Ready? Let's begin!**"
    )
    await m.reply_photo(photo=start_ph, caption=welcome_text)

@bot.on_message(filters.command("stop"))
async def stop_handler(_, m):
    await m.reply_text("🚦BOT STOPPED🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command("txt"))
async def txt_handler(bot: Client, m: Message):
    editable = await m.reply_text("📂 Send your `.txt` file for download.")
    input_msg: Message = await bot.listen(editable.chat.id)
    file_path = await input_msg.download()
    file_name, ext = os.path.splitext(os.path.basename(file_path))

    # decrypt if encrypted
    if file_name.startswith("encrypted_"):
        file_path = helper.decrypt_file_txt(file_path)
        await input_msg.delete(True)

    await editable.edit("Processing your file...")
    with open(file_path, "r") as f:
        content = [line.strip() for line in f.read().splitlines() if line.strip()]
    os.remove(file_path)

    await editable.edit(f"Total links found: **{len(content)}**. Send initial index to start (default=1)")
    input_index = await bot.listen(editable.chat.id)
    start_index = int(input_index.text) if input_index.text.isdigit() else 1
    await input_index.delete(True)

    await editable.edit("Send Batch Name or `df` to use file name:")
    input_batch = await bot.listen(editable.chat.id)
    batch_name = input_batch.text if input_batch.text != "df" else file_name
    await input_batch.delete(True)

    await editable.edit("Enter resolution (1080,720,480,360,240,144):")
    input_res = await bot.listen(editable.chat.id)
    res_map = {"1080": "1920x1080", "720": "1280x720", "480": "854x480",
               "360": "640x360", "240": "426x240", "144": "256x144"}
    resolution = res_map.get(input_res.text, "1280x720")
    await input_res.delete(True)

    await editable.edit("Enter caption text or `df` for default:")
    input_caption = await bot.listen(editable.chat.id)
    CR_text = input_caption.text if input_caption.text != "df" else CR
    await input_caption.delete(True)

    await editable.edit("Send token for pw mpd links or `no`:")
    input_token = await bot.listen(editable.chat.id)
    token = input_token.text if input_token.text != "no" else ""
    await input_token.delete(True)

    await editable.edit("Send custom thumbnail URL or `no`:")
    input_thumb = await bot.listen(editable.chat.id)
    thumb_url = input_thumb.text
    await input_thumb.delete(True)
    await editable.delete()

    if thumb_url.startswith("http"):
        getstatusoutput(f"wget '{thumb_url}' -O 'thumb.jpg'")
        thumb_path = "thumb.jpg"
    else:
        thumb_path = None

    count = start_index
    for link in content[start_index-1:]:
        try:
            # Extract name and url
            name1, url = link.split(":", 1)
            url = url.strip()
            name_clean = re.sub(r'[^\w\-]', '', name1)[:60]

            # Detect file type
            if ".pdf" in url:
                file_type = "pdf"
            elif any(url.endswith(ext) for ext in [".mp4", ".mkv"]):
                file_type = "mp4"
            elif any(url.endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
                file_type = "jpg"
            elif ".mp3" in url:
                file_type = "mp3"
            elif ".html" in url:
                file_type = "html"
            else:
                file_type = "mp4"  # default

            caption = get_captions(file_type, count, name1, resolution, batch_name, url)

            # Download and send logic
            if "drive" in url or ".pdf" in url:
                downloaded_file = await helper.download(url, f"{name_clean}.{file_type}")
                await bot.send_document(chat_id=m.chat.id, document=downloaded_file, caption=caption, parse_mode="html")
                os.remove(downloaded_file)
            elif ".jpg" in url:
                subprocess.run(['wget', url, '-O', f'{name_clean}.jpg'], check=True)
                await bot.send_photo(chat_id=m.chat.id, photo=f'{name_clean}.jpg', caption=caption)
                os.remove(f'{name_clean}.jpg')
            else:
                # yt-dlp / m3u8 / video links
                await helper.download_m3u8_proxy(url, f"{name_clean}.mp4")
                await bot.send_video(chat_id=m.chat.id, video=f"{name_clean}.mp4", caption=caption)
                os.remove(f"{name_clean}.mp4")

            count += 1
            await asyncio.sleep(1)
        except FloodWait as e:
            await m.reply_text(f"FloodWait: {str(e)}. Waiting {e.x}s")
            await asyncio.sleep(e.x)
            continue
        except Exception as e:
            await m.reply_text(f"Error: {str(e)}")
            continue

# -------------------- RUN BOT --------------------
bot.run()
