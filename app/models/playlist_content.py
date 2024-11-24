from __future__ import annotations

from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class PlaylistContent(BaseModel):
    playlist_id: str
    playlist_name: str
    track_id: str
    track_name: str
    added_at: Optional[datetime]
    times_played: int
