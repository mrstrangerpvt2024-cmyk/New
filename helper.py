import os
import subprocess
from urllib.parse import unquote
import aiohttp
import aiofiles
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
import re
import requests

# Encryption keys
KEY = b'^#^#&@*HDU@&@*()'
IV = b'^@%#&*NSHUE&$*#)'

# --- URL Decryption ---
def dec_url(enc_url: str) -> str:
    """Decrypt a helper:// URL."""
    enc_url = enc_url.replace("helper://", "")
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted = unpad(cipher.decrypt(b64decode(enc_url)), AES.block_size)
    return decrypted.decode('utf-8')

def split_name_enc_url(line: str):
    """Split line into name and encrypted URL."""
    match = re.search(r"(helper://\S+)", line)
    if match:
        name = line[:match.start()].strip().rstrip(":")
        enc_url = match.group(1).strip()
        return name, enc_url
    return line.strip(), None

def decrypt_file_txt(input_file: str) -> str:
    """Decrypt all helper:// URLs in a txt file."""
    output_file = f"decrypted_{input_file}"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(input_file, "r", encoding="utf-8") as f, open(output_file, "w", encoding="utf-8") as out:
        for line in f:
            name, enc_url = split_name_enc_url(line)
            if enc_url:
                out.write(f"{name}: {dec_url(enc_url)}\n")
            else:
                out.write(line.strip() + "\n")
    return output_file

# --- PDF / Video Downloads ---
async def aio_download(url: str, filename: str) -> str:
    """Async download file from URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(filename, 'wb') as f:
                    await f.write(await resp.read())
                return filename
            else:
                raise ValueError(f"Download failed with status {resp.status}")

def download_pdf_proxy(url: str, name="Downloaded_File.pdf") -> str | None:
    """Download PDF via RWA proxy."""
    try:
        decoded = unquote(url)
        if "rwa-play-on.vercel.app/pdf" not in decoded:
            print("❌ Not a supported PDF link:", decoded)
            return None
        print(f"🔽 Downloading PDF from {decoded}")
        r = requests.get(decoded, allow_redirects=True, timeout=120)
        r.raise_for_status()
        with open(name, "wb") as f:
            f.write(r.content)
        print(f"✅ Saved as {name}")
        return name
    except Exception as e:
        print("⚠️ PDF download error:", e)
        return None

def download_m3u8_proxy(url: str, name="Downloaded_Video.mp4") -> str | None:
    """Download video via RWA proxy using ffmpeg."""
    try:
        decoded = unquote(url)
        if "rwa-play-on.vercel.app/proxy" not in decoded:
            print("❌ Not a supported m3u8 proxy:", decoded)
            return None
        print(f"🎥 Downloading video from {decoded}")
        cmd = f'ffmpeg -y -i "{decoded}" -c copy -bsf:a aac_adtstoasc "{name}"'
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ Video saved as {name}")
        return name
    except Exception as e:
        print("⚠️ Video proxy download error:", e)
        return None
