
__all__ = ["USER_ID_URL", "PLAYLIST_URL", "SONG_ID_URL", "COMMENTS_URL", "USER_ID_URL_V2"]
# 根据昵称搜索个人用户id url https://music.163.com/weapi/cloudsearch/get/web?csrf_token=
USER_ID_URL = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="

# 获取个人歌单列表信息url
PLAYLIST_URL = "https://music.163.com/weapi/user/playlist?csrf_token="

# 获取歌曲信息url
SONG_ID_URL = "http://music.163.com/weapi/v3/playlist/detail?csrf_token="

# 获取评论 url
COMMENTS_URL = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_"


# 根据昵称获取 用户名id 备用
USER_ID_URL_V2 = 'https://api.imjad.cn/cloudmusic/?type=search&search_type=1002&s='
