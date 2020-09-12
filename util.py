import os
from lxml import etree
import requests
import hashlib
from config import *
import urllib
import json
import base64


def get_form_ck_from_cookie():
    # 从cookie中获取ck值（ck: post操作表单隐藏字段）
    douban_cookies = get_cookies()
    return douban_cookies["ck"]


def get_image_and_id(text):
    # 通过html提取验证码图片URL和id
    html = etree.HTML(text)
    pic_url = html.xpath("//img[@id='captcha_image']/@src")
    pic_id = html.xpath("//input[@name='captcha-id']/@value")
    if len(pic_url) and len(pic_id):
        return pic_url[0], pic_id[0]
    else:
        return "", ""


def get_verify_code_pic(session, url):
    # 获取验证码的图片URL和id

    r = session.get(url, cookies=get_cookies())
    if r.status_code == 200:
        pic_url, pic_id = get_image_and_id(r.text)
        print(str(pic_url))
        return pic_url, pic_id
    else:
        print(str(url) + ", status_code: " + str(r.status_code))
        return "", ""


def get_access_token():
    # 获取百度AI开放平台的access_token

    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials' \
           '&client_id=' + API_KEY + '&client_secret=' + SECRET_KEY
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    content = response.read()
    if content:
        content = json.loads(content)
    return content


def get_word_in_pic(pic_path):
    # 给定图片地址 pic_path，识别图片当中的文字
    result = get_access_token()
    access_token = result["access_token"]
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/webimage?access_token=' + access_token
    # 二进制方式打开图文件
    f = open(pic_path, 'rb')
    # 参数image：图像base64编码
    img = base64.b64encode(f.read())
    params = {"image": img}
    params = urllib.parse.urlencode(params).encode(encoding="utf-8")
    request = urllib.request.Request(url, params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib.request.urlopen(request)
    content = response.read()
    f.close()
    os.remove(pic_path)
    if content:
        print("baidu OCR API returns: " + str(content))
        content = json.loads(content)
        words_result = content["words_result"]
        if len(words_result):
            words = str(words_result[0]["words"]).strip()
            return words.split(" ")[0]
        else:
            return ""
    else:
        return ""


def get_cookies():
    cookies = {}
    with open('cookies.txt', "r", encoding='utf-8') as f_cookie:
        douban_cookies = f_cookie.readlines()[0].split("; ")
        for line in douban_cookies:
            key, value = line.split("=", 1)
            cookies[key] = value
        return cookies


def flush_cookies(session: requests.Session):
    cookies = session.cookies.get_dict()
    line = ""
    with open('cookies.txt', "w", encoding='utf-8') as f_cookie:
        for k, v in cookies.items():
            line += k + '=' + v + '; '
        line = line[:len(line) - 2]
        f_cookie.write(line)


def save_pic_to_disk(pic_url, session):
    # 将链接中的图片保存到本地，并返回文件名
    try:
        res = session.get(pic_url)
        if res.status_code == 200:
            # 求取图片的md5值，作为文件名，以防存储重复的图片
            md5_obj = hashlib.md5()
            md5_obj.update(res.content)
            md5_code = md5_obj.hexdigest()
            file_name = img_path + str(md5_code) + ".jpg"
            # 如果图片不存在，则保存
            if not os.path.exists(file_name):
                with open(file_name, "wb") as f:
                    f.write(res.content)
            return file_name
        else:
            print("in func save_pic_to_disk(), fail to save pic. pic_url: " + pic_url +
                  ", res.status_code: " + str(res.status_code))
            raise Exception
    except Exception as e:
        print(e)
