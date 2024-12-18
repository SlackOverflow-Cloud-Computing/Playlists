from fastapi import Depends, FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# from app.routers import spotify
from app.routers import playlists

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)


# app.include_router(spotify.router)
app.include_router(playlists.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
