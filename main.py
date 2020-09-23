import request_wrapper
import time
from random import choice
from group_spider import get_group_posts
from group_post import *
# from rss_parser import parse_weibo
from apscheduler.schedulers.blocking import BlockingScheduler


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
    copy_post(s, 'https://www.douban.com/group/topic/194810386/', '696739')
    # post_list = parse_weibo()
    # post_in_group(s, post_list[0]['title'], post_list[0]['content'])
    post_list = [
        'https://www.douban.com/group/topic/193453043/',
        'https://www.douban.com/group/topic/193452907/',
        'https://www.douban.com/group/topic/193452829/',
        'https://www.douban.com/group/topic/193453193/',
        # 'https://www.douban.com/group/topic/193154210/'
    ]
    # group_posts_url = [p['link'] for p in get_group_posts('700330')]
    # post_index = [group_posts_url.index(p) for p in post_list]
    # up_post = group_posts_url[max(post_index)]
    # reply_content_list = ['UP!', '顶顶', 'up', 'dd', '你不能糊', 'Up', '给我上去', '绝绝绝']
    # reply_to_post(s, up_post, choice(reply_content_list) + ' by a bot at ' + time.asctime(time.localtime()))

    util.flush_cookies(s)


if __name__ == '__main__':
    main()
    # sched = BlockingScheduler()
    # sched.add_job(main, 'interval', hours=1, start_date='2020-9-12 21:00:00', end_date='2020-9-24 23:00:00')
    # sched.start()
