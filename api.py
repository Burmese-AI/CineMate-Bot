import os
from typing import Optional, Union

import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

def fetch_genres() -> Optional[dict[int, str]]:
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

def fetch_movies(genre_id: int) -> Optional[list[dict[str, Union[str, float]]]]:
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "with_genres": genre_id,
        "sort_by": "popularity.desc",
        "language": "en-US",
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            movies = [{
                "title": movie["title"],
                "poster_url": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie['poster_path'] else None,
                "overview": movie["overview"],
                "rating": movie["vote_average"],
                "release_year": movie["release_date"].split("-")[0] if movie["release_date"] else "N/A"
            } for movie in data.get("results", [])[:10]]
            return movies
        else:
            print(f"Failed to fetch data. HTTP Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching movies from TMDB API: {e}")
        return None


def search_movies(movie_name: str) -> Optional[list[dict[str, Union[str, float]]]]:
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_name,
        "language": "en-US"
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            movies = [{
                "title": movie["title"],
                "poster_url": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie['poster_path'] else None,
                "overview": movie["overview"],
                "rating": movie["vote_average"],
                "release_year": movie["release_date"].split("-")[0] if movie["release_date"] else "N/A"
            } for movie in data.get("results", [])[:5]]
            return movies
        else:
            print(f"Failed to fetch data. HTTP Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error searching for movies on TMDB API: {e}")
        return None
