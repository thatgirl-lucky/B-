import socket
import json
from urllib import parse
import nest_asyncio
nest_asyncio.apply()
from functools import reduce
from hashlib import md5
import urllib.parse
import time
mixinKeyEncTab = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
    36, 20, 34, 44, 52
]
def getMixinKey(orig: str):
    return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, '')[:32]
def encWbi(params: dict, img_key: str, sub_key: str):
    mixin_key = getMixinKey(img_key + sub_key)
    curr_time = round(time.time())
    params['wts'] = curr_time
    params = dict(sorted(params.items()))
    params = {
        k: ''.join(filter(lambda chr: chr not in "!'()*", str(v)))
        for k, v in params.items()
    }
    query = urllib.parse.urlencode(params)
    wbi_sign = md5((query + mixin_key).encode()).hexdigest()
    params['w_rid'] = wbi_sign
    return params

def getWbiKeys():
    head = {
        'Cookie': "",
        'User-Agent': ''
    }
    url='https://api.bilibili.com/x/web-interface/nav'
    resp = requests.get(url,headers=head)
    resp.raise_for_status()
    json_content = resp.json()
    img_url: str = json_content['data']['wbi_img']['img_url']
    sub_url: str = json_content['data']['wbi_img']['sub_url']
    img_key = img_url.rsplit('/', 1)[1].split('.')[0]
    sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
    return img_key, sub_key

def get_query(**parameters: dict):
    img_key, sub_key = getWbiKeys()
    signed_params = encWbi(
        params=parameters,
        img_key=img_key,
        sub_key=sub_key
    )
    query = urllib.parse.urlencode(signed_params)
    return query

def down_personinfo(mid):
    global max_num
    max_num = 6
    for i in range(max_num):
        try:
            query = get_query(mid=mid, platform='web', web_location=XXXXX)
            url = f'https://api.bilibili.com/x/space/wbi/acc/info?{query}'
            head = {
                'Cookie': "",
                'User-Agent': ''
            }
            res = requests.get(url, headers=head)
            return res

        except socket.timeout as e1:
            print(e1)
            return -1
def get_text(aid, ps=30, pn=1):
    try:
        query = get_query(mid=aid, platform='web', web_location=XXXX, ps=ps, pn=pn, order='click',
                          keyword='')##XXXXX替换成自己的
        url = f"https://api.bilibili.com/x/space/wbi/arc/search?{query}"
        head = {
            'Cookie': "",
            'User-Agent': ''
        }
        response = requests.get(url, headers=head)
        tx = response.text
        return tx
        json_tx = json.loads(tx)
        if json_tx['code'] != 0:
            return -1
    except:
        tx = requests.get(url, headers=head).text
        json_tx = json.loads(tx)
        if json_tx['code'] != 0:
            return -1
    return tx
import requests

def main():
    mid = ''  # 替换为实际的用户ID
    user_info_response = down_personinfo(mid)
    if user_info_response != -1:
        print("用户基本信息：")
        print(user_info_response.text)
    else:
        print("获取用户信息失败")

    video_info_text = get_text(mid)
    if video_info_text != -1:
        print("视频信息：")
        print(video_info_text)
    else:
        print("获取视频信息失败")

if __name__ == "__main__":
    main()
