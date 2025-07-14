"""FastAPI simple microservice."""

import argparse
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from src.common.env import Settings
from src.handlers.recommend import make_recommendation
from src.model import SimilarityModel
from src.models.recommend import RecommendationRequest, RecommendationResponse

app = FastAPI()
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=[os.environ.get("TRUSTED_HOST", "*")]
)
settings = Settings()


@app.get("/")
async def root():
    return {"message": "Recommender-Backend"}


@app.get("/healthz")
async def health_route():
    return {"message": "healthy", "status": 200}


@app.post("/recommend")
async def recommend_route(rec_request: RecommendationRequest) -> RecommendationResponse:
    ids = make_recommendation(rec_request.tmdb_id, model, settings)
    if ids is None:
        ids = []
    return RecommendationResponse(status=200, data=ids)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port", "-p", default=8000, help="the port to run the recommender API on"
    )
    parser.add_argument("--model", "-m", help="path to the model")
    args = parser.parse_args()

    model = SimilarityModel(args.model)
    model.load()

    uvicorn.run(app, host="0.0.0.0", port=int(args.port))
