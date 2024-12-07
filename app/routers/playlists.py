from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.models.user import User
from app.models.playlist import Playlist
from app.services.service_factory import ServiceFactory
import dotenv, os

dotenv.load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

@router.get("/playlists/{playlist_id}", tags=["playlists"])
async def get_playlist(playlist_id: str, token: str = Depends(oauth2_scheme)) -> Playlist:
    service = ServiceFactory.get_service("Playlist")
    if not service.validate_token(token, scope=("/playlists/{playlist_id}", "GET")):
        raise HTTPException(status_code=401, detail="Invalid Token")

    return service.get_playlist(playlist_id)


@router.post("/playlist/{playlist_id}", tags=["playlists"])
async def update_playlist(playlist: Playlist, token: str = Depends(oauth2_scheme)):
    service = ServiceFactory.get_service("Playlist")
    if not service.validate_token(token, scope=("/playlist/{playlist_id}", "POST")):
        raise HTTPException(status_code=401, detail="Invalid Token")

    service.update_playlist(playlist)


@router.delete("/playlist/{playlist_id}", tags=["playlists"])
async def delete_playlist(playlist_id: str):
    service = ServiceFactory.get_service("Playlist")
    if not service.validate_token(token, scope=("/playlist/{playlist_id}", "DELETE")):
        raise HTTPException(status_code=401, detail="Invalid Token")

    service.delete_playlist(playlist_id)


@router.get("/playlists/{user_id}", tags=["playlists"])
async def get_playlists(user_id: str) -> List[Playlist]:
    service = ServiceFactory.get_service("Playlist")
    if not service.validate_token(token, scope=("/playlists/{user_id}", "GET")):
        raise HTTPException(status_code=401, detail="Invalid Token")

    return service.get_playlists(user_id)
