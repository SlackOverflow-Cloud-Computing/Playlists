from dotenv import load_dotenv
import os

from framework.services.service_factory import BaseServiceFactory
from app.services.spotify_api import SpotifyAPIService


# Load environment variables from .env file
load_dotenv()

class ServiceFactory(BaseServiceFactory):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_service(cls, service_name):

        match service_name:
            case "SpotifyAPIService":
                client_id = os.getenv("SPOTIFY_CLIENT_ID")
                client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
                result = SpotifyAPIService(client_id, client_secret)

            case _:
                result = None

        return result
