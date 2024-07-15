from typing import Dict, Optional

import requests

from .config import TMDB_API_KEY


def fetch_genres() -> Optional[Dict[int, str]]:
    url = "https://api.themoviedb.org/3/genre/movie/list"
    params = {
        "api_key": TMDB_API_KEY,
        "sort_by": "popularity.desc",
        "language": "en-US",
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            genres = data.get("genres", [])
            if genres:
                return {genre['id']: genre['name'] for genre in genres}
            else:
                print("No genres found in the response.")
                return None
        else:
            print(f"Failed to fetch data. HTTP Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching genres from TMDB API: {e}")
        return None
