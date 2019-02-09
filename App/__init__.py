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
        pass

    def request_user_playlist(self, user_id):
        """
        request playlist
        :param user_id: str
        :return: [playlist_id1, playlist_id2, playlist_id3....playlist_idn]
        """
        pass

    def request_user_songs_list(self):
        """
        request all songs according to playlist
        :param playlist: [playlist_id1, playlist_id2, playlist_id3....playlist_idn]
        :return: [song_id_1, song_id2, song_id3, ... , song_idn]
        """
        pass

    def request_user_comments(self):
        """
        request and compare infomation then write it to mysql
        :param song_id: str
        :return: None
        """
        pass


class RequestInfo(Request):
    def __init__(self, username):
        super().__init__()
        self.match_data = {}
        self.username = username
        self.playlist_id = []
        self.song_id = []

    def _parse_playlist_id(self, data):
        info = list()
        # todo :add solve playlist function in get playlist_id
        return info

    def _parse_user_id(self, data):
        """parse userid in return data"""
        # todo :add solve user function
        id = str()
        return None

    def _parse_song_id(self, data):
        # todo :add solve song function
        ids = list()
        return ids

    def _parse_comments_id(self, data):
        """IF exists username-comment group then add it to the match_data """
        for comment in data:
            if comment['user']['nickname'] == self.username:
                self.match_data[data['song_name']] = comment["content"]
        else:
            pass

    def request_user_id(self):
        headers, payload = netease_encryptor.generate_requests_info()
        catch_data = requests.post(USER_ID_URL, headers=headers, payload=payload)
        return self._parse_user_id(data=catch_data)

    def request_user_playlist(self, user_id):
        """get all playlist id and add all of them into self.playlist_id """
        headers, payload = netease_encryptor.generate_requests_info()
        catch_data = requests.post(PLAYLIST_URL, headers=headers, payload=payload)
        self.playlist_id = self._parse_playlist_id(data=catch_data)

    def request_user_songs_list(self):
        """get all song id and add all of them into self.song_id"""
        headers, payload = netease_encryptor.generate_requests_info()
        for single in self.playlist_id:
            catch_data = requests.post(SONG_ID_URL, headers=headers, payload=payload)
            self.song_id.append(self._parse_song_id(data=catch_data))

    def request_user_comments(self):
        for single in self.song_id:
            headers, payload = netease_encryptor.generate_requests_info()
            catch_data = requests.post(SONG_ID_URL, headers=headers, payload=payload)
            self._parse_song_id(data=catch_data)

    def return_match(self):
        return self.match_data

    def get_info(self):
        # all execute code in here

        pass
