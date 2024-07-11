from fastapi import FastAPI
from .api.routes import users, games, ai_personalities, cards, history

app = FastAPI(title="Cards Against AI")

app.include_router(users.router, tags=["users"], prefix="/api")
app.include_router(games.router, tags=["games"], prefix="/api")
app.include_router(ai_personalities.router, tags=["ai_personalities"], prefix="/api")
app.include_router(cards.router, tags=["cards"], prefix="/api")
app.include_router(history.router, tags=["history"], prefix="/api")


@app.get("/")
async def root():
    return {"message": "Welcome to Cards Against AI"}
