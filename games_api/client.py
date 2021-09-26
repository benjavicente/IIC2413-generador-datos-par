import os
import json

from igdb.wrapper import IGDBWrapper


class Client:
    def __init__(self) -> None:
        self._wrapper = IGDBWrapper(
            client_id=os.getenv("TWITCH_CLIENT"),
            auth_token=os.getenv("TWITCH_ACCESS_TOKEN"),
        )

    def _json_query(self, endpoint: str, query: str):
        response_bytes = self._wrapper.api_request(endpoint, query)
        return json.loads(response_bytes)

    def get_games(self, query: str):
        return self._json_query("games", query)

    def get_external_games(self, query: str):
        return self._json_query("external_games", query)
