import requests
from App.requests_info.url import *
from App.encrypt import netease_encryptor
from concurrent import futures

class Request(object):
    def __init__(self):
        pass

    def request_user_id(self):
        """
        request user_id according to username
        :param username:str
        :return: str
        """
        raise NotImplemented

    def request_user_playlist(self):
        """
        request playlist
        :param user_id: str
        :return: [playlist_id1, playlist_id2, playlist_id3....playlist_idn]
        """
        raise NotImplemented

    def request_user_songs_list(self):
        """
        request all songs according to playlist
        :param playlist: [playlist_id1, playlist_id2, playlist_id3....playlist_idn]
        :return: [song_id_1, song_id2, song_id3, ... , song_idn]
        """
        raise NotImplemented

    def request_user_comments(self):
        """
        request and compare infomation then write it to mysql
        :param song_id: str
        :return: None
        """
        raise NotImplemented


class RequestInfo(Request):
    def __init__(self, username):
        super().__init__()
        self.match_data = {}
        self.username = username
        self.playlist_id = []
        self.song_id = []
        self.MAX_WORKERS = 20

    @property
    def user_id(self):
        return self.user_ids

    @property
    def comments(self):
        return self.match_data

    @property
    def songs(self):
        return self.song_id

    @property
    def playlist(self):
        return self.playlist_id

    def _parse_playlist_id(self, data):
        return [c['id'] for c in data['playlist'] if c['userId'] == self.user_id]

    def _parse_user_id(self, data):
        """parse userid in return data"""
        id = str()
        id = data['result']["userprofiles"][0]["userId"]
        return id

    def _parse_song_id(self, data):
        self.song_id += [c['id'] for c in data['playlist']['trackIds']]

    def _parse_comments_id(self, data):
        """IF exists username-comment group then add it to the match_data """
        for comment in data:
            if comment['user']['nickname'] == self.username:
                print("匹配成功， 结果为:", comment["content"] )
                self.match_data[data['song_name']] = comment["content"]
                flag = True


    def request_user_id(self):
        headers, payload = netease_encryptor.generate_requests_info(key=self.username, type=1002)
        catch_data = requests.post(USER_ID_URL, headers=headers, data=payload).json()
        self.user_ids = self._parse_user_id(data=catch_data)

    def request_user_playlist(self):
        """get all playlist id and add all of them into self.playlist_id """
        headers, payload = netease_encryptor.generate_requests_info(uid=self.user_id, limit=100, offset=1, i=1)
        catch_data = requests.post(url=PLAYLIST_URL, headers=headers, data=payload).json()
        self.playlist_id = self._parse_playlist_id(data=catch_data)

    def request_user_songs_list(self):
        """
        get all song id and add all of them into self.song_id
        """
        def post_data(id):
            headers, payload = netease_encryptor.generate_requests_info(id=id)
            catch_data = requests.post(SONG_ID_URL, headers=headers, data=payload).json()
            self._parse_song_id(data=catch_data)
        if len(self.playlist_id) == 0:
            raise Exception("用户歌单数等于0")
        workers = min(self.MAX_WORKERS, len(self.playlist_id))
        with futures.ThreadPoolExecutor(workers) as executor:
            executor.map(post_data, self.playlist_id)


    def request_user_comments(self):
        def post_data(i, single):
            """获取单页数据"""
            headers, payload = netease_encryptor.generate_requests_info(i=int(i),offset=10)
            catch_data = requests.post(COMMENTS_URL+single + "?crsf=", headers=headers, data=payload).json()
            if "msg" in catch_data.keys() and catch_data['msg'] == 'Cheating':
                    raise Exception("ip封杀")
            self._parse_comments_id(data=catch_data['comments'])


        def get_comment_numbers(single):
            headers, payload = netease_encryptor.generate_requests_info(i=1, offset=20)
            catch_data = requests.post(COMMENTS_URL+single+"?crsf=", headers=headers, data=payload).json()
            return int(catch_data['total'])


        for single in self.song_id:
            # 请求第一次 数据  获取评论总量
            single = str(single)
            all_number = get_comment_numbers(single=single)
            pages = all_number / 10
            print("当前页数:",pages, "当前歌曲id", single)
            page = [i for i in range(int(pages-1))]
            single_list = [single]*int(pages-1)
            workers = min(self.MAX_WORKERS, pages)
            with futures.ThreadPoolExecutor(workers) as executor:
                res = executor.map(post_data, page, single_list)




