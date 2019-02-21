import json
import os
import base64
import codecs

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA


class NeteaseEncrypt(object):
    modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    nonce = '0CoJUm6Qyw8W8jud'
    pubKey = '010001'

    def __init__(self):
        self.params = ['i', "offset", "user_id", "type", "s", "limit", "total", "album_id", "id", "c", "br", "uid"]

    def generate_header(self):
        """
        you can add headers in here
        :return: dict
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        return headers

    def aesEncrypt(self, text, secKey):
        pad = 16 - len(text) % 16
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        text = text + str(pad * chr(pad))
        encryptor = AES.new(secKey, 2, '0102030405060708')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext

    def rsaEncrypt(self, data: str, publickey: str, module: str):
        """
        RSA采用Nopadding方式，即明文先倒排，再在前面补0
        data:明文
        publickey:公钥
        module:RSA中两个大质数的乘积
        """
        # 网易云云音乐中js加密采用的算法中的参数是以16进制来操作的
        _publickey = int(publickey, 16)
        _module = int(module, 16)
        _data = data[::-1]
        _data = int(codecs.encode(_data.encode('utf8'), 'hex'), 16)
        # RSA加密过程
        rs = _data ** _publickey % _module
        # 返回16进制解码，前面补0补足256位的字符串
        return format(rs, 'x').zfill(256)

    def createSecretKey(self, size):
        return (''.join(map(lambda xx: (hex(ord(xx))[2:]), str(os.urandom(size)))))[0:16]

    def generate_requests_info(self, **kwargs):
        text_dict = {
            "username": "",
            "password": "",
            "remenberLogin": "true"
        }
        for x in kwargs.keys():
            if x not in self.params:
                raise Exception("params error")
            text_dict[x] = kwargs[x]
        if "offset" in kwargs:
            text_dict['i'] = int(kwargs['offset'] / 10)
        text = json.dumps(text_dict)
        secKey = self.createSecretKey(16)
        encText = self.aesEncrypt(self.aesEncrypt(text, self.nonce), secKey)
        encSecKey = self.rsaEncrypt(secKey, self.pubKey, self.modulus)
        payload = {'params': encText, 'encSecKey': encSecKey}
        return self.generate_header(), payload


netease_encryptor = NeteaseEncrypt()
