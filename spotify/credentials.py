import json
from pathlib import Path

path = Path(__file__).resolve().parent.joinpath("creds.json")
with open(path) as f:
    creds = json.load(f)

REDIRECT_URL = creds.get("REDIRECT_URL")
CLIENT_SECRET = creds.get("CLIENT_SECRET")
CLIENT_ID = creds.get("CLIENT_ID")

