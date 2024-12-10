import dotenv, os
from typing import Any, List
from requests import delete

import jwt
from pyexpat.errors import messages
from turtledemo.sorting_animate import enable_keys

from framework.resources.base_resource import BaseResource

from app.models.playlist_content import PlaylistContent
from app.models.playlist_info import PlaylistInfo

dotenv.load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = "HS256"

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


    def validate_token(self, token: str, scope: tuple[str, str]) -> bool:
        """Checks if the token is valid for the given scope"""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
            if scope[1] not in payload.get("scopes").get(scope[0]):
                return False
            else:
                return True

        except jwt.exceptions.InvalidTokenError:
            return False


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

    def get_playlists(self, user_id: str) -> List[PlaylistInfo]:
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


                key_fields = ["playlist_id", "track_id"]
                key_values = [playlist_content.playlist_id, playlist_content.track_id]
                if_existed = d_service.get_data_object_with_multiple_keys(
                    self.database, self.content_collection, key_fields=key_fields, key_values=key_values,
                )
                if if_existed:
                    return {"status": "success",
                            "message": f"Playlist content {playlist_content.track_id} already exists."}

                content_data = playlist_content.model_dump()
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
        if_content_existed = d_service.get_data_object(
            self.database, self.content_collection, key_field=self.content_key_field, key_value=playlist_id,
        )
        delete_content = d_service.delete_data_object(
            self.database, self.content_collection, key_field=self.content_key_field, key_value=playlist_id
        )
        delete_info = d_service.delete_data_object(
            self.database, self.info_collection, key_field=self.info_key_field, key_value=playlist_id
        )

        if delete_info and delete_content:
            return {"status": "success", "message": f"Playlist {playlist_id} and its content have been deleted."}
        elif delete_info and not delete_content and not if_content_existed:
            return {"status": "success", "message": f"Playlist {playlist_id} has been deleted but there's no content in the playlist."}
        else:
            return {"status": "error", "message": f"Failed to delete playlist {playlist_id} or its content."}

    def delete_song(self, playlist_id: str, track_id: str):
        d_service = self.data_service
        key_fields = ["playlist_id", "track_id"]
        key_values = [playlist_id, track_id]
        delete_info = d_service.delete_data_object_with_multiple_keys(
            self.database, self.content_collection, key_fields=key_fields, key_values=key_values
        )
        if delete_info:
            return {"status": "success", "message": f"The song {track_id} in Playlist {playlist_id} has been deleted."}
        else:
            return {"status": "error", "message": f"Failed to delete song {track_id}."}

    def create_branch(self, playlist_id: str, branch_id: str):
        pass

    def set_branch(self, branch_id: str):
        pass
