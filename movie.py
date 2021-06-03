import os
import requests


class MovieService:

    def __init__(self) -> None:
        self.base_url = f'https://api.themoviedb.org/3/search/movie?api_key={os.environ.get("MOVIE_API_KEY")}&language=en-US'

    def search_movie(self, search: str):
        query_params = {
            'query': search,
            'page': 1
        }
        try:
            response = requests.get(self.base_url, query_params)
            if response.status_code == 200:
                data = response.json().get('results')
                return self._create_movie_options(data)
        except Exception as e:
            print(f"Error publishing home tab: {e}")

    def _create_movie_options(self, data):
        result = []
        for movie in data:
            result.append({"text": {"type": "plain_text", "text": movie.get(
                "title")}, "value": str(movie.get("id"))})
        return result


# m = MovieService()
# m.search_movie('fight')
