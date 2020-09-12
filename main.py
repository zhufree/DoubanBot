import request_wrapper
import util
import time
from random import choice
# from rss_parser import parse_weibo
from apscheduler.schedulers.blocking import BlockingScheduler


def reply_to_post(session, url, content):
    reply_url = url + 'add_comment'
    pic_url, pic_id = util.get_verify_code_pic(session, url)
    verify_code = ""
    if len(pic_url):
        pic_path = util.save_pic_to_disk(pic_url, session)
        verify_code = util.get_word_in_pic(pic_path)
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
    # print(r.text)


def post_in_group(session, title, content):
    # 组装发帖需要的参数
    publish_url = 'https://www.douban.com/j/group/topic/publish'
    topic_new_url = 'https://www.douban.com/group/696739/new_topic'
    pic_url, pic_id = util.get_verify_code_pic(session, topic_new_url)
    verify_code = ""
    if len(pic_url):
        pic_path = util.save_pic_to_disk(pic_url)
        verify_code = util.get_word_in_pic(pic_path)
    topic_dict = {
        "ck": util.get_form_ck_from_cookie(),
        "title": title,
        "content": "{'blocks':[{'key':'893dl','text':'" + content
                   + '''','type':'unstyled','depth':0,'inlineStyleRanges':[],'entityRanges':[],
                   'data':{'page':0}}],'entityMap':{}}''',
        "captcha-solution": verify_code,
        "captcha-id": pic_id,
        "group_id": 696739
    }
    print(topic_dict)
    r = session.post(publish_url, topic_dict)


def main():
    req_wrapper = request_wrapper.ReqWrapper()
    s = req_wrapper.session
    s.headers.update({
        'Host': 'www.douban.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    })
    s.cookies.update(util.get_cookies())
    # 启动循环
    # 解析rss，寻找可以发的帖
    # 发帖后记录，避免重复发帖
    # post_list = parse_weibo()
    # post_in_group(s, post_list[0]['title'], post_list[0]['content'])
    post_list = [
        'https://www.douban.com/group/topic/193453043/',
        'https://www.douban.com/group/topic/193452907/',
        'https://www.douban.com/group/topic/193452829/',
        'https://www.douban.com/group/topic/193453193/',
    ]
    reply_content_list = ['UP!', 'UP', 'up', 'dd', 'DD', 'Up']
    for i in post_list:
        reply_to_post(s, i, choice(reply_content_list))
        print('reply: ' + i)
        time.sleep(60)

    util.flush_cookies(s)


if __name__ == '__main__':
    # main()
    sched = BlockingScheduler()
    sched.add_job(main, 'cron', day='*', hour='*')
    sched.start()