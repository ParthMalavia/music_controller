import json

creds = json.loads("creds.json")

REDIRECT_URL = creds.get("REDIRECT_URL")
CLIENT_SECRET = creds.get("CLIENT_SECRET")
CLIENT_ID = creds.get("CLIENT_ID")

