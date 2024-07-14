from fastapi import FastAPI
from .api.routes import users, games, ai_personalities, cards, history

app = FastAPI(title="Cards Against AI API", version="1.0.1")

app.include_router(users.router, tags=["users"])
app.include_router(games.router, tags=["games"])
app.include_router(ai_personalities.router, tags=["ai_personalities"])
app.include_router(cards.router, tags=["cards"])
app.include_router(history.router, tags=["history"])


@app.get("/")
async def root():
    return {"message": "Welcome to Cards Against AI API"}
