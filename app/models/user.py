from __future__ import annotations

from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[datetime] = None  # Date format as string
    password: Optional[str] = None
    # phone_number: Optional[str] = None
    # last_login: Optional[str] = None  # Date format as string
    # session_token: Optional[str] = None
    # ip_address: Optional[str] = None
    # device_info: Optional[str] = None
    # updated_at: Optional[str] = None  # Date format as string
