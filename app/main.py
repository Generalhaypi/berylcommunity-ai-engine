from __future__ import annotations

from fastapi import FastAPI
from app.api.routes_community import router as community_router


app = FastAPI(
    title="BerylCommunity API",
    version="1.0.0"
)


# On branche les routes Community sur le préfixe /community
app.include_router(community_router, prefix="/community", tags=["community"])


@app.get("/health", tags=["health"])
async def healthcheck():
    """Lightweight health endpoint."""
    return {"status": "ok"}
