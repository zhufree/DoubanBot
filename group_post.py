import util
import os
from pyquery import PyQuery as pq

spider_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.117 Safari/537.36'}


def reply_to_post(session, url, content):
    reply_url = url + 'add_comment'
    pic_url, pic_id = util.get_verify_code_pic(session, url)
    verify_code = ""
    if len(pic_url):
        retry_count = 0
        while verify_code == '' and retry_count < 5:  # 识别不出的话重试
            pic_path = util.save_pic_to_disk(pic_url, session)
            verify_code = util.get_word_in_pic(pic_path)
            os.remove(pic_path)
            retry_count = retry_count + 1

    reply_dict = {
        "ck": util.get_form_ck_from_cookie(),
        'rv_comment': content,
        "captcha-solution": verify_code,
        "captcha-id": pic_id,
        'start': 0,
        'submit_btn': '发送'
    }
    print(reply_dict)
    session.post(reply_url, reply_dict)
    # print('reply: ' + url)
    # print(r.text)


def post_in_group(session, group_id, title, content):
    # 组装发帖需要的参数
    publish_url = 'https://www.douban.com/j/group/topic/publish'
    topic_new_url = 'https://www.douban.com/group/%s/new_topic' % group_id
    pic_url, pic_id = util.get_verify_code_pic(session, topic_new_url)
    verify_code = ""
    if len(pic_url):
        pic_path = util.save_pic_to_disk(pic_url)
        verify_code = util.get_word_in_pic(pic_path)
    topic_dict = {
        "ck": util.get_form_ck_from_cookie(),
        "title": title,
        "content": r"{'blocks':[{'key':'893dl','text':'" + content.strip()
                   + '''','type':'unstyled','depth':0,'inlineStyleRanges':[],'entityRanges':[],data':{'page':0}}],'entityMap':{}}''',
        "captcha-solution": verify_code,
        "captcha-id": pic_id,
        "group_id": 696739
    }

    print(topic_dict)
    r = session.post(publish_url, topic_dict)
    print(r.text)


def copy_post(session, post_url, to_group_id):
    doc = pq(post_url, headers=spider_header)
    title = doc('.article>h1').text()
    print(title)
    post_in_group(session, to_group_id, title, post_url)
