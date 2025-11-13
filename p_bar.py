import time
from datetime import timedelta
from pyrogram.errors import FloodWait

class Timer:
    def __init__(self, time_between=1):  # Reduce delay for faster updates
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False


def hrb(value, digits=2, delim="", postfix=""):
    """Human-readable file size"""
    if value is None:
        return None
    chosen_unit = "B"
    for unit in ("KiB", "MiB", "GiB", "TiB"):
        if value > 1024:
            value /= 1024
            chosen_unit = unit
        else:
            break
    return f"{value:.{digits}f}{delim}{chosen_unit}{postfix}"


def hrt(seconds, precision=0):
    """Human-readable time delta"""
    pieces = []
    value = timedelta(seconds=int(seconds))

    if value.days:
        pieces.append(f"{value.days}d")

    seconds = value.seconds

    if seconds >= 3600:
        hours = int(seconds / 3600)
        pieces.append(f"{hours}h")
        seconds -= hours * 3600

    if seconds >= 60:
        minutes = int(seconds / 60)
        pieces.append(f"{minutes}m")
        seconds -= minutes * 60

    if seconds > 0 or not pieces:
        pieces.append(f"{seconds}s")

    if not precision:
        return "".join(pieces)

    return "".join(pieces[:precision])


timer = Timer()


async def progress_bar(current, total, reply, start):
    if not timer.can_send():
        return

    now = time.time()
    diff = now - start
    if diff < 0.5:  # minimum 0.5s between updates for smoothness
        return

    perc = f"{current * 100 / total:.1f}%"
    elapsed_time = max(diff, 0.1)
    speed = current / elapsed_time
    remaining_bytes = total - current
    eta = hrt(remaining_bytes / speed, precision=1) if speed > 0 else "-"

    sp = str(hrb(speed)) + "/s"
    tot = hrb(total)
    cur = hrb(current)

    bar_length = 12  # slightly longer for better visualization
    completed_length = int(current * bar_length / total)
    progress_bar_str = "▰" * completed_length + "▱" * (bar_length - completed_length)

    text = (
        f"📦 Upload Status\n\n"
        f"📁 Upload Root\n"
        f"├── 🐼 WELCOME: ᑌᑭᒪOᗩᗪᗴᖇ ACTIVE\n"
        f"│   ├── 📊 Progress: {progress_bar_str} {perc}\n"
        f"│   ├── ⚡ Speed: {sp}\n"
        f"│   ├── 🗂️ Loaded: {cur} / {tot}\n"
        f"│   └── ⏳ ETA: {eta}\n"
        f"└── 🚀 Bot By: SAKSHAM"
    )

    try:
        await reply.edit(text)
    except FloodWait as e:
        time.sleep(e.x)
