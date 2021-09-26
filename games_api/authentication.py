import os
import requests


def load_access_token():
    auth_params = {
        "client_id": os.getenv("TWITCH_CLIENT"),
        "client_secret": os.getenv("TWITCH_SECRET"),
        "grant_type": "client_credentials",
    }
    response = requests.post("https://id.twitch.tv/oauth2/token", json=auth_params)
    data = response.json()
    if "access_token" in data:
        os.environ["TWITCH_ACCESS_TOKEN"] = data["access_token"]
    else:
        raise ConnectionError("Couldn't obtain the access token")
