from framework.services.service_factory import BaseServiceFactory
from app.services.playlist import PlaylistService
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
            case "Playlist":
                result = PlaylistService(client_id, client_secret)

            case _:
                result = None

        return result
