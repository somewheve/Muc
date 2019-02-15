__all__ = ["USER_ID_URL", "PLAYLIST_URL", "SONG_ID_URL", "COMMENTS_URL"]

# search userid according username
USER_ID_URL = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="

# get the playlist ids
PLAYLIST_URL = "https://music.163.com/weapi/user/playlist?csrf_token="

# get all song ids
SONG_ID_URL = "http://music.163.com/weapi/v3/playlist/detail?csrf_token="

# get all comments
COMMENTS_URL = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_"
