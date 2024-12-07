from framework.services.service_factory import BaseServiceFactory
import dotenv, os
import app.resources.playlist_resource as playlist_resource
from framework.services.data_access.MySQLRDBDataService import MySQLRDBDataService


dotenv.load_dotenv()
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
host = os.getenv('DB_HOST')
port = int(os.getenv('DB_PORT'))

class ServiceFactory(BaseServiceFactory):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_service(cls, service_name):

        if service_name == 'PlaylistResource':
            result = playlist_resource.PlaylistResource(config=None)
        elif service_name == 'PlaylistResourceDataService':
            context = dict(user=user, password=password, host=host, port=port)
            data_service = MySQLRDBDataService(context=context)
            result = data_service
        else:
            result = None


        return result
