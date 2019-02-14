import json
import os
from Crypto.Cipher import AES
import base64
import codecs


class NeteaseEncrypt(object):
    modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    nonce = '0CoJUm6Qyw8W8jud'
    pubKey = '010001'

    def generate_header(self):
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

    def rsaEncrypt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def createSecretKey(self, size):
        return (''.join(map(lambda xx: (hex(ord(xx))[2:]), str(os.urandom(size)))))[0:16]

    def generate_requests_info(self, **kwargs):
        text_dict = {
            "username": "",
            "password": "",
            "remenberLogin": "true"
        }

        if "i" and "offset" in kwargs.keys():
            offset = kwargs['offset']
            i = kwargs['i']
            text_dict["offset"] = i* offset
        if "user_id" in kwargs.keys():
            text_dict['user_id'] = kwargs['user_id']
        if "type" in kwargs.keys():
            text_dict["type"] = kwargs['type']
        if "key" in kwargs.keys():
            text_dict['s'] = kwargs['key']
        if "limit" in kwargs.keys():
            text_dict['limit'] = kwargs['limit']
        if "total" in kwargs.keys():
            text_dict['total'] = kwargs['total']
        if "album_id" in kwargs.keys():
            text_dict["album_id"] = kwargs['album_id']
        if "id" in kwargs.keys():
            text_dict['id'] = kwargs["id"]
        if "c" in kwargs.keys():
            text_dict['c'] = kwargs["c"]
        if "br" in kwargs.keys():
            text_dict['br'] = kwargs['br']
        if "uid" in kwargs.keys():
            text_dict['uid'] = kwargs['uid']

        text = json.dumps(text_dict)
        secKey = self.createSecretKey(16)
        encText = self.aesEncrypt(self.aesEncrypt(text,self.nonce), secKey)
        encSecKey = self.rsaEncrypt(secKey, self.pubKey, self.modulus)
        payload = {'params': encText, 'encSecKey': encSecKey}
        return self.generate_header(), payload


netease_encryptor = NeteaseEncrypt()
