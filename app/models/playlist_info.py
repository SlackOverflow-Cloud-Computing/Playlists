from __future__ import annotations

from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class PlaylistInfo(BaseModel):
    playlist_id: str
    playlist_name: str
    user_id: str
    user_name: str
    created_at: Optional[datetime]
    times_played: int
