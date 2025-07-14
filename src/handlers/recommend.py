"""The recommendation handler."""

from typing import List

from src.common.env import Settings
from src.model import SimilarityModel
from src.tmdb.api import get_movie


def make_recommendation(
    movie_id: int, model: SimilarityModel, settings: Settings
) -> List[int]:
    """Make predictions based off of an entered TMDB ID."""
    data = get_movie(movie_id, settings)
    ids = model.infer(movie_id, [data], top_k=5)
    return ids
