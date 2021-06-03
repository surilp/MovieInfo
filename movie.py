import os
import requests
from conf import IMG_BASE_URL, MOVIE_SERVICE_BASE_URL
from util import convert_date


class MovieService:

    def __init__(self) -> None:
        self.query_param = {
            "api_key": os.environ.get("MOVIE_API_KEY"),
            "language": "en-US"
        }

    def search_movie(self, search: str):
        params = self.query_param.copy()
        params.update(
            {
                "query": search,
                "page": 1
            }
        )
        try:
            response = requests.get(
                f"{MOVIE_SERVICE_BASE_URL}/search/movie", params)
            if response.status_code == 200:
                data = response.json().get("results")
                return self._create_movie_options(data)
        except Exception as e:
            print(f"Error publishing home tab: {e}")

    def get_movie_detail(self, movie_id):
        try:
            response = requests.get(
                f"{MOVIE_SERVICE_BASE_URL}/movie/{movie_id}", self.query_param)
            if response.status_code == 200:
                data = response.json()
                return self._extract_movie_detail(data, ["title", "poster_path", "release_date", "overview"])
        except Exception as e:
            print(f"Error publishing home tab: {e}")

    def _create_movie_options(self, data):
        result = []
        for movie in data:
            result.append({"text": {"type": "plain_text", "text": movie.get(
                "title")}, "value": str(movie.get("id"))})
        return result

    def _extract_movie_detail(self, data, required_attribute):
        result = {}
        for attribute in required_attribute:
            if attribute in data:
                if attribute == "poster_path":
                    result[attribute] = f"{IMG_BASE_URL}{data[attribute]}"
                elif attribute == "release_date":
                    result[attribute] = convert_date(data[attribute])
                else:
                    result[attribute] = data[attribute]
        return result
