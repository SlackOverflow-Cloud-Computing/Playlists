from fastapi import APIRouter, status, HTTPException

from pydantic import BaseModel

from app.models.playlist_content import PlaylistContent
from app.models.playlist_info import PlaylistInfo
from app.models.user import User
from app.models.token import Token
from app.services.service_factory import ServiceFactory
import dotenv, os

from typing import List

dotenv.load_dotenv()
router = APIRouter()

@router.get("/playlist/{playlist_id}", tags=["playlists"])
async def get_playlist(playlist_id: str) -> PlaylistInfo:
    service = ServiceFactory.get_service("PlaylistResource")
    playlist = service.get_playlist(playlist_id)
    if playlist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found")
    return playlist

@router.get("/playlists/{user_id}", tags=["playlists"])
async def get_playlists(user_id: str) -> List[PlaylistInfo]:
    service = ServiceFactory.get_service("PlaylistResource")
    playlists = service.get_playlists(user_id)
    if playlists is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlists not found")
    return playlists

@router.post("/update/{playlist_id}", tags=["playlists"])
async def update_playlist(playlist_info: PlaylistInfo, playlist_content: PlaylistContent):
    service = ServiceFactory.get_service("PlaylistResource")
    result = service.update_playlist(playlist_info, playlist_content)
    if result.get("status") == "success":
        return {"message": result.get("message")}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Failed to update playlist.")
        )

@router.delete("/{playlist_id}", tags=["playlists"])
async def delete_playlist(playlist_id: str):
    service = ServiceFactory.get_service("PlaylistResource")
    if service.get_playlist(playlist_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found")

    result = service.delete_playlist(playlist_id)
    if result.get("status") == "success":
        return {"message": result.get("message")}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Failed to delete playlist.")
        )

@router.delete("/{playlist_id}/{track_id}", tags=["playlists"])
async def delete_song(playlist_id: str, track_id: str):
    service = ServiceFactory.get_service("PlaylistResource")
    result = service.delete_song(playlist_id, track_id)
    if result.get("status") == "success":
        return {"message": result.get("message")}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Failed to delete song.")
        )


# @router.post("/branch/{playlist_id}/{branch_id}", tags=["playlists"])
# async def create_branch(playlist_id: str, branch_id: str):
#     service = ServiceFactory.get_service("PlaylistResource")
#     service.create_branch(playlist_id, branch_id)
#
# @router.post("/playlist/{playlist_id}/branch/{branch_id}", tags=["playlists"])
# async def set_branch(branch_id: str):
#     service = ServiceFactory.get_service("PlaylistResource")
#     service.set_branch(branch_id)
