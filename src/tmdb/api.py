"""Get all needed information from TMDB"""

import json
from typing import List, Optional

import requests
from ratelimit import limits

from src.common.env import Settings
from src.common.logger import get_logger


logger = get_logger(__name__)

BASE_URL = "https://api.themoviedb.org/3"


@limits(calls=40, period=2)
def get_movie(tmdb_id: List[int], settings: Settings) -> Optional[List[dict]]:
    """Enrich the data from letterboxd with data from TMDB.

    Args:
        None
    Returns:
        None
    Raises:
        RuntimeError if self.movies is not set
    """
    try:
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {settings.tmdb_access_token}",
        }
        response = requests.get(
            f"{BASE_URL}/movie/{tmdb_id}?language=en-US", headers=headers, timeout=120
        )
        if response.status_code != 200:
            logger.error(f"request failed with {response.text}")
            return None
        resp = json.loads(response.text)
        genres = resp["genres"]
        genres = [x["name"] for x in genres]
        original_title = resp["original_title"]
        overview = resp["overview"]
        ret_text = original_title + " " + overview + " " + " ".join(genres)
        return ret_text  # type:ignore[no-any-return]
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(f"failed parsing {tmdb_id} - {e}")
        return None
