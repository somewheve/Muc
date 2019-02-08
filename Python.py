import requests
import json
import time
import os
import logging
from Crypto.Cipher import AES
import base64
import codecs
from process import ShowProcess

logging.basicConfig(level=logging.WARNING)




def get_it_comments(nickname="西瓜醋l", url="", nums=1500):
    cat = int(nums) / 10
    offset = 10
    result = {"result": 0, "nickname": nickname, "contents": None}
    global always
    # 进度条
    process_bar = ShowProcess(int(cat), "获取完成")

    for i in range(int(cat)):
        time.sleep(0.01)
        process_bar.show_process(i)
        # 一个i获取10个评论
        headers, payload = netease_encryptor.generate_requests_info(i=i, offset=offset)
        r = requests.post(url, headers=headers, data=payload)
        r.raise_for_status()
        try:
            r_dic = json.loads(r.text)
        except:
            logging.warning("json.loads(r.text)出错了")
        comments = r_dic["comments"]
        for comment in comments:
            info = {}
            info['nickname'] = comment['user']['nickname']
            info['contents'] = comment["content"]
            if info['nickname'] == nickname:
                result['result'] = 1
                result['nickname'] = nickname
                result['contents'] = info['contents']
                return result
            always.append(info)
    return result


def generate_url(songid="1317868860"):
    return 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + songid + '?csrf_token='


if __name__ == '__main__':
    logging.warning("欢迎使用云音乐评论查询工具" + "*" * 50)
    logging.warning("请输入对应参数")
    logging.warning("按下回车开始输入")
    result_map = {1: "成功", 0: "失败"}
    input()
    nickname = input("昵称: ")
    nums = input("查找范围: ")
    song_id = input("歌曲号(in url): ")
    logging.warning("*" * 61)
    logging.warning("开始查询")
    logging.warning("进度条:")
    url = generate_url(songid=song_id)
    query_result = get_it_comments(url=url, nickname=nickname, nums=nums)

    logging.critical(
        "\n查询结果: {} \n查询用户: {} \n查询内容: {}".format(result_map[query_result['result']], query_result['nickname'],
                                                  query_result['contents']))
    with open("result.json", "w") as fp:
        cko = {}
        cko['result'] = query_result
        fp.write(json.dumps(cko))


# 根据昵称搜索个人用户id url https://music.163.com/weapi/cloudsearch/get/web?csrf_token=

# 获取个人歌单列表信息url  https://music.163.com/weapi/user/playlist?csrf_token=

# 获取歌曲信息url https://music.163.com/#/playlist?id=2483161318

# 获取评论 url http://music.163.com/weapi/v1/resource/comments/R_SO_4_




