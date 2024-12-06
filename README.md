# Playlist Service
Service for managing anything to do with playlists


## Usage

You need to configure a .env file with your Spotify App information like this:

```
```

Note: This services works with S3 for blob storage.

`uvicorn app.main:app --reload --port 8008`

This services currently runs on `http://127.0.0.1:8008` by default for testing.
