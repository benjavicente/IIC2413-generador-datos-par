import games_api
from pprint import pprint
import json


def fetch_games(limit: int = 1):
    client = games_api.Client()

    # https://apicalypse.io/syntax/
    query = f"""
        fields
            name, genres.name, themes.name, platforms.platform_family.name,
            themes.name, first_release_date, summary, age_ratings.category,
            age_ratings.rating, total_rating, platforms.name;
        where total_rating_count != null;
        sort total_rating_count desc;
        limit {limit};
    """
    games = client.get_games(query)

    if limit < 5:
        pprint(games, width=120)
    else:
        with open("data_dump.json", "w", encoding="utf-8") as file:
            json.dump(games, file, ensure_ascii=False)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("amount", type=int, help="Cantidad de datos a obtener")
    args = parser.parse_args()
    fetch_games(args.amount)
