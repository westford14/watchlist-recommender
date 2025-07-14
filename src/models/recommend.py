"""Models for the recommendation handler."""

from typing import List

from pydantic import BaseModel


class RecommendationRequest(BaseModel):
    """Recommendation request model."""

    tmdb_id: int


class RecommendationResponse(BaseModel):
    """Recommendation response model."""

    status: int
    data: List[int]
