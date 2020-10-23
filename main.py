import request_wrapper
from group_spider import get_group_posts
from group_post import *
# from rss_parser import parse_weibo


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
    get_group_posts('707438')
    util.flush_cookies(s)


if __name__ == '__main__':
    main()
    # sched = BlockingScheduler()
    # sched.add_job(main, 'interval', hours=1, start_date='2020-9-12 21:00:00', end_date='2020-9-24 23:00:00')
    # sched.start()
