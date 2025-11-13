import os

try:
    API_ID = int(os.environ["22470912"])
except KeyError:
    raise RuntimeError("❌ Environment variable API_ID not set!")

try:
    API_HASH = os.environ["511be78079ed5d4bd4c967bc7b5ee023"]
except KeyError:
    raise RuntimeError("❌ Environment variable API_HASH not set!")

try:
    BOT_TOKEN = os.environ["7254519583:AAHCuy42E2GbwNFzfUF1Gjt5oBAoOy_i7Kw"]
except KeyError:
    raise RuntimeError("❌ Environment variable BOT_TOKEN not set!")
