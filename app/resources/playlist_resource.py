from turtledemo.sorting_animate import enable_keys
from typing import Any, List

from pyexpat.errors import messages

from framework.resources.base_resource import BaseResource

from app.models.playlist_content import PlaylistContent
from app.models.playlist_info import PlaylistInfo
from app.models.user import User
from app.models.token import Token
import dotenv, os

dotenv.load_dotenv()
db = os.getenv('DB_NAME')
info_collection = os.getenv('DB_INFO_COLLECTION')
content_collection = os.getenv('DB_CONTENT_COLLECTION')


class PlaylistResource(BaseResource):

    def __init__(self, config):
        super().__init__(config)

        from app.services.service_factory import ServiceFactory # Temporary solution
        self.data_service = ServiceFactory.get_service("PlaylistResourceDataService")
        self.database = db
        self.info_collection = info_collection
        self.content_collection = content_collection
        self.info_key_field = "playlist_id"
        self.content_key_field = 'playlist_id'

    def get_by_key(self, key: str):

        d_service = self.data_service
        result = d_service.get_data_object(
            self.database, self.info_collection, key_field=self.info_key_field, key_value=key
        )
        return result

    def get_playlist(self, playlist_id: str) -> PlaylistInfo:
        d_service = self.data_service
        result = d_service.get_data_object(
            self.database, self.info_collection, key_field=self.info_key_field, key_value=playlist_id,
            fetch_all=False
        )
        if result:
            result = PlaylistInfo(**result)
        return result

    def get_playlists(self, user_id: str):
        d_service = self.data_service
        result = d_service.get_data_object(
            self.database, self.info_collection, key_field="user_id", key_value=user_id,
            fetch_all=True
        )
        # print(result)
        playlists = []
        if result:
            for item in result:
                playlists.append(PlaylistInfo(**item))
        return playlists


    def update_playlist(self, playlist_info: PlaylistInfo, playlist_content: PlaylistContent=None):
        d_service = self.data_service
        if_existed = d_service.get_data_object(
            self.database, self.info_collection, key_field=self.info_key_field, key_value=playlist_info.playlist_id
        )
        if if_existed is None:
            # If the playlist does not exist, add a new playlist info and the content
            try:
                info_data = playlist_info.model_dump()
                add_info = d_service.add_data_object(self.database, self.info_collection, data=info_data)
                add_content = True
                if playlist_content is not None:
                    content_data = playlist_content.model_dump()
                    add_content = d_service.add_data_object(self.database, self.content_collection, data=content_data)

                if add_info and add_content:
                    return {"status": "success", "message": f"Playlist {playlist_info.playlist_id} has been added."}
                else:
                    return {"status": "error", "message": f"Failed to add playlist {playlist_info.playlist_id}."}
            except Exception as e:
                print(f"Failed to create playlist: {e}")
        else:
            # If the playlist already exists, update the content
            try:
                if playlist_content is None:
                    return {"status": "success",
                            "message": f"Playlist {playlist_info.playlist_id} exists, no content to update."}

                content_data = playlist_content.model_dump()
                # TODO: check if the content already exists, by using playlist_id and track_id
                add_content = d_service.add_data_object(
                    self.database,
                    self.content_collection,
                    data=content_data,
                )
                if add_content:
                    return {"status": "success", "message": f"Playlist {playlist_info.playlist_id} has been updated."}
                else:
                    return {"status": "error", "message": f"Failed to update playlist {playlist_info.playlist_id}."}
            except Exception as e:
                print(f"Failed to update playlist: {e}")


    def delete_playlist(self, playlist_id: str):
        d_service = self.data_service
        delete_content = d_service.delete_data_object(
            self.database, self.content_collection, key_field=self.content_key_field, key_value=playlist_id
        )
        delete_info = d_service.delete_data_object(
            self.database, self.info_collection, key_field=self.info_key_field, key_value=playlist_id
        )

        if delete_info and delete_content:
            return {"status": "success", "message": f"Playlist {playlist_id} and its content have been deleted."}
        else:
            return {"status": "error", "message": f"Failed to delete playlist {playlist_id} or its content."}

    # TODO: delete the song from the content table
    def delete_song(self, playlist_id: str, track_id: str):
        pass


    def create_branch(self, playlist_id: str, branch_id: str):
        pass

    def set_branch(self, branch_id: str):
        pass



