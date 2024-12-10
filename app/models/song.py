from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

class Song(BaseModel):
    track_id: Optional[str] = None
    track_name: Optional[str] = None
    track_artist: Optional[str] = None
    track_popularity: Optional[float] = None
    track_album_id: Optional[str] = None
    track_album_name: Optional[str] = None
    track_album_release_date: Optional[str] = None
    playlist_name: Optional[str] = None
    playlist_id: Optional[str] = None
    playlist_genre: Optional[str] = None
    playlist_subgenre: Optional[str] = None
    danceability: Optional[float] = None
    energy: Optional[float] = None
    key: Optional[float] = None
    loudness: Optional[float] = None
    mode: Optional[float] = None
    speechiness: Optional[float] = None
    acousticness: Optional[float] = None
    instrumentalness: Optional[float] = None
    liveness: Optional[float] = None
    valence: Optional[float] = None
    tempo: Optional[float] = None
    duration_ms: Optional[float] = None

    class Config:
        json_schema_extra = {
            "example": {
                "track_id": "6f807x0ima9a1j3VPbc7VN",
                "track_name": "I Don't Care (with Justin Bieber) - Loud Luxury Remix",
                "track_artist": "Ed Sheeran",
                "track_popularity": 66,
                "track_album_id": "2oCs0DGTsRO98Gh5ZSl2Cx",
                "track_album_name": "I Don't Care (with Justin Bieber) [Loud Luxury Remix]",
                "track_album_release_date": "2019-06-14",
                "playlist_name": "Pop Remix",
                "playlist_id": "37i9dQZF1DXcZDD7cfEKhW",
                "playlist_genre": "pop",
                "playlist_subgenre": "dance pop",
                "danceability": 0.748,
                "energy": 0.916,
                "key": 6,
                "loudness": -2.634,
                "mode": 1,
                "speechiness": 0.0583,
                "acousticness": 0.102,
                "instrumentalness": 0,
                "liveness": 0.0653,
                "valence": 0.518,
                "tempo": 122.036,
                "duration_ms": 194754
            }
        }
