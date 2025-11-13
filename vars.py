import os

try:
    API_ID = int(os.environ["API_ID"])
except KeyError:
    raise RuntimeError("22470912")

try:
    API_HASH = ["API_HASH"]
except KeyError:
    raise RuntimeError("511be78079ed5d4bd4c967bc7b5ee023")

try:
    BOT_TOKEN = os.environ["BOT_TOKEN"]
except KeyError:
    raise RuntimeError("7254519583:AAHCuy42E2GbwNFzfUF1Gjt5oBAoOy_i7Kw")
