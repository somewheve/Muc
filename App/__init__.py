# coding:utf-8
from concurrent import futures
from pprint import pprint
from functools import wraps

import requests

from App.requests_info.url import *
from App.encrypt import netease_encryptor


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
        self.user_id = None
        self.check_map = {"song": self.song_id, "playlist": self.playlist_id, "username": self.username}

    @property
    def userid(self):
        return self.user_id

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
                pprint("match successful， result:", comment["content"])
                self.match_data[data['song_name']] = comment["content"]
                flag = True

    # it should be example method , not classmethod
    def check(self, func=None, **kwargs):
        type = kwargs['type']
        if type not in self.check_map.keys():
            raise Exception("error decoration")

        destionation = self.check_map[type]
        if len(destionation) != 0 or destionation is not None:
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper
        raise Exception("error in invoking,please check {} is Empty or length = 0".format(type))

    @check(type="username")
    def request_user_id(self):
        headers, payload = netease_encryptor.generate_requests_info(key=self.username, type=1002)
        catch_data = requests.post(USER_ID_URL, headers=headers, data=payload).json()
        self.user_id = self._parse_user_id(data=catch_data)

    @check(type="userid")
    def request_user_playlist(self):
        """get all playlist id and add all of them into self.playlist_id """
        headers, payload = netease_encryptor.generate_requests_info(uid=self.user_id, limit=100, offset=1, i=1)
        catch_data = requests.post(url=PLAYLIST_URL, headers=headers, data=payload).json()
        self.playlist_id = self._parse_playlist_id(data=catch_data)

    @check(type="playlist")
    def request_user_songs_list(self):
        """
        get all song id and add all of them into self.song_id
        """

        def post_data(id):
            headers, payload = netease_encryptor.generate_requests_info(id=id)
            catch_data = requests.post(SONG_ID_URL, headers=headers, data=payload).json()
            self._parse_song_id(data=catch_data)

        workers = min(self.MAX_WORKERS, len(self.playlist_id))
        with futures.ThreadPoolExecutor(workers) as executor:
            executor.map(post_data, self.playlist_id)

    @check(type="song")
    def request_user_comments(self):
        def post_data(i, single):
            """get simple page data"""
            headers, payload = netease_encryptor.generate_requests_info(i=int(i), offset=10)
            catch_data = requests.post(COMMENTS_URL + single + "?crsf=", headers=headers, data=payload).json()
            if "msg" in catch_data.keys() and catch_data['msg'] == 'Cheating':
                raise Exception("ip has been forbidden")
            self._parse_comments_id(data=catch_data['comments'])

        def get_comment_numbers(single):
            headers, payload = netease_encryptor.generate_requests_info(i=1, offset=20)
            catch_data = requests.post(COMMENTS_URL + single + "?crsf=", headers=headers, data=payload).json()
            return int(catch_data['total'])

        for single in self.song_id:
            # get the count of all comments
            single = str(single)
            all_number = get_comment_numbers(single=single)
            pages = all_number / 10
            page = [i for i in range(int(pages - 1))]
            single_list = [single] * int(pages - 1)
            print(len(page), "-", len(single_list))
            workers = min(self.MAX_WORKERS, pages)
            with futures.ThreadPoolExecutor(workers) as executor:
                res = executor.map(post_data, page, single_list)
