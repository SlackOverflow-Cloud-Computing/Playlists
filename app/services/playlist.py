import os
import requests
import base64

import jwt
from fastapi import FastAPI, HTTPException, Request
from pydantic import ValidationError

from app.models.user import User
from app.models.token import Token


JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = "HS256"


class PlaylistService:

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret


    def validate_token(self, token: Token, scope: tuple[str, str]) -> bool:
        """Checks if the token is valid for the given scope"""
        try:
            payload = jwt.decode(token.access_token, JWT_SECRET, algorithms=[ALGORITHM])
            if scope[1] not in payload.get("scopes").get(scope[0]):
                return False
            else:
                return True

        except jwt.exceptions.InvalidTokenError:
            return False


    def login(self, auth_code, redirect_uri) -> Token:
        url = "https://accounts.spotify.com/api/token"

        # Prepare the authorization header (Base64 encoded client_id:client_secret)
        auth_header = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()

        # Prepare the POST data for the token request
        token_data = {
            'code': auth_code,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }

        headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # Send a POST request to Spotify to exchange the authorization code for tokens
        try:
            response = requests.post(url, data=token_data, headers=headers)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to retrieve token")

            data = response.json()
            # print(f"Login Response: {data}")
            token = Token.parse_obj(data)
            return token

        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error fetching token: {str(e)}")


    def refresh_token(self, token: Token) -> Token:
        # TODO need to refresh stale tokens
        pass

    def get_user_info(self, token: Token) -> User:
        url = "https://api.spotify.com/v1/me"
        headers = {
            "Authorization": f"Bearer {token.access_token}"
        }

        # Send a GET request to the Spotify API
        try:
            response = requests.get(url, headers=headers)

            # Check if the request was successful
            if response.status_code != 200:
                raise Exception(f"Failed to fetch user info: {response.status_code} - {response.text}")

            # Parse the JSON response
            user_data = response.json()

            # Map the relevant fields to your User model
            user = User(
                id=user_data.get("id"),
                username=user_data.get("display_name"),
                email=user_data.get("email"),
                country=user_data.get("country"),
                profile_image=user_data.get("images")[0].get("url") if user_data.get("images") else None,
                created_at=None,
                last_login=None
            )

            return user

        except requests.RequestException as e:
            raise Exception(f"An error occurred while fetching user info: {str(e)}")


    def get_user_playlists(self, token: Token):
