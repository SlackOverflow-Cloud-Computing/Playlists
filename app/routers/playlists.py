from fastapi import APIRouter
from pydantic import BaseModel

from app.models.user import User
from app.models.token import Token
from app.services.service_factory import ServiceFactory
import dotenv, os

dotenv.load_dotenv()
router = APIRouter()

@router.get("/playlist/{playlist_id}", tags=["playlists"])
async def get_playlist(playlist_id: str) -> Playlist:
    service = ServiceFactory.get_service("Playlist")
    playlist = service.get_playlist(playlist_id)
    return playlist

@router.get("/playlists/{user_id}", tags=["playlists"])
async def get_playlists(user_id: str) -> List[Playlist]:
    service = ServiceFactory.get_service("Playlist")
    playlists = service.get_playlists(user_id)
    return playlists

@router.post("/update/{playlist_id}", tags=["playlists"])
async def update_playlist(playlist: Playlist):
    service = ServiceFactory.get_service("Playlist")
    service.update_playlist(playlist)

@router.delete("/{playlist_id}", tags=["playlists"])
async def delete_playlist(playlist_id: str):
    service = ServiceFactory.get_service("Playlist")
    service.delete_playlist(playlist_id)

@router.post("/branch/{playlist_id}/{branch_id}", tags=["playlists"])
async def create_branch(playlist_id: str, branch_id: str):
    service = ServiceFactory.get_service("Playlist")
    service.create_branch(playlist_id, branch_id)

@router.post("/playlist/{playlist_id}/branch/{branch_id}", tags=["playlists"])
async def set_branch(branch_id: str):
    service = ServiceFactory.get_service("Playlist")
    service.set_branch(branch_id)
