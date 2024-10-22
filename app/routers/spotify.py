from fastapi import APIRouter
from pydantic import BaseModel

from app.models.user import User
from app.models.token import Token
from app.services.service_factory import ServiceFactory

REDIRECT_URI = "http://localhost:3000/auth"

router = APIRouter()

class LoginRequest(BaseModel):
    auth_code: str

class LoginResponse(BaseModel):
    user: User
    token: Token


@router.post("/login", tags=["users"])
async def login(request: LoginRequest) -> LoginResponse:
    api_service = ServiceFactory.get_service("SpotifyAPIService")
    token = api_service.login(request.auth_code, REDIRECT_URI)
    user = api_service.get_user_info(token)
    return LoginResponse(user=user, token=token)
