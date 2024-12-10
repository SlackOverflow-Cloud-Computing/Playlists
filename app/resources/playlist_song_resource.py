import dotenv, os
from typing import Any, List as TypingList
from requests import delete

from framework.resources.base_resource import BaseResource

from app.models.playlist_content import PlaylistContent
from app.models.playlist_info import PlaylistInfo
from app.models.song import Song

from sqlalchemy import create_engine, Column, String as SQLAlchemyString, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from graphene import ObjectType, Field, String, List, NonNull
from graphene_sqlalchemy import SQLAlchemyObjectType


# Playlist database connections
dotenv.load_dotenv()
db_playlist = os.getenv('DB_NAME')
info_collection = os.getenv('DB_INFO_COLLECTION')
content_collection = os.getenv('DB_CONTENT_COLLECTION')

# Spotify songs database connections
db_song = os.getenv('DB_NAME_SONG')
song_collection = os.getenv('DB_SONG_COLLECTION')

from app.services.service_factory import ServiceFactory  # Temporary solution
data_service = ServiceFactory.get_service("PlaylistResourceDataService")

Base = declarative_base()

class PlaylistInfo(Base):
    __tablename__ = 'playlist_info'
    playlist_id = Column(SQLAlchemyString, primary_key=True)
    playlist_name = Column(SQLAlchemyString)
    user_id = Column(SQLAlchemyString)

class PlaylistContent(Base):
    __tablename__ = 'playlist_content'
    playlist_id = Column(SQLAlchemyString, primary_key=True)
    track_id = Column(SQLAlchemyString, primary_key=True)

class Song(Base):
    __tablename__ = 'song'
    track_id = Column(SQLAlchemyString, primary_key=True)
    track_name = Column(SQLAlchemyString)
    track_artist = Column(SQLAlchemyString)


class PlaylistInfoType(SQLAlchemyObjectType):
    class Meta:
        model = PlaylistInfo

class PlaylistContentType(SQLAlchemyObjectType):
    class Meta:
        model = PlaylistContent
        only_fields = ("playlist_id", "track_id")

class SpotifySongType(SQLAlchemyObjectType):
    class Meta:
        model = Song
        only_fields = ("track_id", "track_name", "track_artist")


# GraphQL Query Definition
class Query(ObjectType):
    tracks_by_playlist = List(SpotifySongType, playlist_id=NonNull(String))

    def resolve_tracks_by_playlist(self, info, playlist_id) -> TypingList[Song]:
        try:
            tracks = data_service.get_data_object(
                db_playlist, content_collection, key_field="playlist_id", key_value=playlist_id, fetch_all=True
            )
            if not tracks:
                return []

            track_ids = [track['track_id'] for track in tracks]

            songs = []
            for track_id in track_ids:
                song = data_service.get_data_object(
                db_song, song_collection, key_field="track_id", key_value=track_id
            )
                songs.append(song)
            if not songs:
                return []

            print(f"Playlist {playlist_id} songs detail: {songs}")

            return [
                Song(
                    track_id=song["track_id"],
                    track_name=song["track_name"],
                    track_artist=song["track_artist"]
                )
                for song in songs
            ]

        except Exception as e:
            print(f"Error resolving tracks_by_playlist for playlist_id {playlist_id}: {e}")
            return []



# FastAPI application integration
# from fastapi import FastAPI
# from starlette_graphene3 import GraphQLApp
# from graphene import Schema
#
# app = FastAPI()
# schema = Schema(query=Query)
# app.add_route("/graphql", GraphQLApp(schema=schema))