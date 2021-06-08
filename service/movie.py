import os
import requests
from conf import IMG_BASE_URL, MOVIE_SERVICE_BASE_URL
from util import convert_date
import logging

class MovieService:

    def __init__(self) -> None:
        self.query_param = {
            "api_key": os.environ.get("MOVIE_API_KEY"),
            "language": "en-US"
        }

    def search_movie(self, search: str) -> list:
        """This function does lazy search by calling service to support typeahead componenet on the UI

        Args:
            search (str): lazy movie search

        Returns:
            list: returns list of movies based on search string
        """
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
            logging.error(f"Error searching movie - {search}: {e}")

    def get_movie_detail(self, movie_id: str) -> dict:
        """This function retrieves movie detail for movie id passed in as parameter

        Args:
            movie_id (str): movie id

        Returns:
            dict: movie detail
        """
        try:
            response = requests.get(
                f"{MOVIE_SERVICE_BASE_URL}/movie/{movie_id}", self.query_param)
            if response.status_code == 200:
                data = response.json()
                return self._extract_movie_detail(data, ["title", "poster_path", "release_date", "overview"])
            else:
                logging.error(f"Movie detail request for movie id: {movie_id} was not successful. Status Code: {response.status_code}")
        except Exception as e:
            logging.error(f"Error getting movie detail for movie id - {movie_id}: {e}")

    def _create_movie_options(self, data: list) -> list:
        """This function takes raw data returned from service and transforms it to format needed for select menu

        Args:
            data (list): service returned data

        Returns:
            list: transformed data
        """
        result = []
        for movie in data:
            result.append({"text": {"type": "plain_text", "text": movie.get(
                "title")}, "value": str(movie.get("id"))})
        return result

    def _extract_movie_detail(self, data: dict, required_attribute: list) -> dict:
        """This function transform movie detail object to only needed attribute object.

        Args:
            data (dict): service returned data
            required_attribute (list): needed attribute list

        Returns:
            dict: transformed data
        """
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
