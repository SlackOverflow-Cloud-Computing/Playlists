from framework.services.service_factory import BaseServiceFactory
from app.services.spotify_api import SpotifyAPIService
import dotenv, os

dotenv.load_dotenv()
client_id = os.getenv('SPOTIFY_CLIENT_ID') 
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')


class ServiceFactory(BaseServiceFactory):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_service(cls, service_name):

        match service_name:
            case "SpotifyAPIService":
                client_id = client_id
                client_secret = client_secret
                result = SpotifyAPIService(client_id, client_secret)

            case _:
                result = None

        return result
