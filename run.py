from App import RequestInfo

if __name__ == '__main__':
    info = RequestInfo("西瓜醋l")
    info.request_user_id()
    info.request_user_playlist()
    info.request_user_songs_list()
    print(len(info.song_id))
    info.request_user_comments()
    print(info.comments)

