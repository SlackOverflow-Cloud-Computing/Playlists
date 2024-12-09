import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

from app.models.playlist_content import PlaylistContent
from app.models.playlist_info import PlaylistInfo
from app.services.service_factory import ServiceFactory
import dotenv, os

from typing import List

dotenv.load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

log_dir = "C:\\var\\log"
os.makedirs(log_dir, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "playlists.log")),  # Log file
        logging.StreamHandler()  # Also log to the console
    ]
)

logger = logging.getLogger("uvicorn")
router = APIRouter()

@router.get("/playlists/{playlist_id}", tags=["playlists"])
async def get_playlist(playlist_id: str, token: str = Depends(oauth2_scheme)) -> PlaylistInfo:
    logger.info(f"Incoming Request - Method: GET, Path: /playlists/{playlist_id}")
    service = ServiceFactory.get_service("PlaylistResource")
    if not service.validate_token(token, scope=("/playlists/{playlist_id}", "GET")):
        raise HTTPException(status_code=401, detail="Invalid Token")

    playlist = service.get_playlist(playlist_id)
    if playlist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found")
    return playlist


@router.post("/playlists/{playlist_id}", tags=["playlists"])
async def update_playlist(playlist_info: PlaylistInfo, playlist_content: PlaylistContent, token: str = Depends(oauth2_scheme)):
    logger.info(f"Incoming Request - Method: POST, Path: /playlist/{playlist_info.playlist_id}")
    service = ServiceFactory.get_service("PlaylistResource")
    if not service.validate_token(token, scope=("/playlists/{playlist_id}", "POST")):
        raise HTTPException(status_code=401, detail="Invalid Token")

    result = service.update_playlist(playlist_info, playlist_content)
    if result.get("status") == "success":
        return {"message": result.get("message")}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Failed to update playlist.")
        )


@router.delete("/playlists/{playlist_id}", tags=["playlists"])
async def delete_playlist(playlist_id: str, token: str = Depends(oauth2_scheme)):
    logger.info(f"Incoming Request - Method: DELETE, Path: /playlist/{playlist_id}")
    service = ServiceFactory.get_service("PlaylistResource")
    if not service.validate_token(token, scope=("/playlists/{playlist_id}", "DELETE")):
        raise HTTPException(status_code=401, detail="Invalid Token")

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


@router.get("/users/{user_id}/playlists", tags=["playlists"])
async def get_user_playlists(user_id: str, token: str = Depends(oauth2_scheme)) -> List[PlaylistInfo]:
    logger.info(f"Incoming Request - Method: GET, Path: /playlists/{user_id}")
    service = ServiceFactory.get_service("PlaylistResource")
    if not service.validate_token(token, scope=("/playlists/{user_id}", "GET")):
        raise HTTPException(status_code=401, detail="Invalid Token")

    return service.get_playlists(user_id)


@router.delete("/playlists/{playlist_id}/tracks/{track_id}", tags=["playlists"])
async def delete_song(playlist_id: str, track_id: str, token: str = Depends(oauth2_scheme)):
    logger.info(f"Incoming Request - Method: DELETE, Path: /playlist/{playlist_id}")

    service = ServiceFactory.get_service("PlaylistResource")
    if not service.validate_token(token, scope=("/playlists/{playlist_id}/{track_id}", "DELETE")):
        raise HTTPException(status_code=401, detail="Invalid Token")

    result = service.delete_song(playlist_id, track_id)
    if result.get("status") == "success":
        return {"message": result.get("message")}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Failed to delete song.")
        )
