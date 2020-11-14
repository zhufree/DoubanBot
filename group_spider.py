from pyquery import PyQuery as pq
import time

spider_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.117 Safari/537.36'}
group_base_url = 'https://www.douban.com/group/'


def get_group_members(group_id):
    member_name_list = []
    member_link_list = []
    start_count = 0
    while start_count <= 5635:
        group_member_url = group_base_url + group_id + '/members?start=%d' % start_count
        doc = pq(group_member_url, headers=spider_header)
        start_count += 35
        for i in doc('.name').items():
            name = i('a').text()
            link = i('a').attr("href")
            member_name_list.append(name)
            member_link_list.append(link)
        time.sleep(5)
    with open('member-%s.txt' % group_id, 'w+', encoding='utf-8') as f:
        f.writelines(member_link_list)


def get_group_posts(group_id):
    post_list = []
    start = 0
    while start < 50:
        group_post_url = group_base_url + group_id + '/discussion?start=%d' % start
        doc = pq(group_post_url, headers=spider_header)
        start += 25
        post_list += [{
            'title': i('a').text(),
            'link': i('a').attr('href'),
            'author': i.siblings().eq(0)('a').text(),
            'author_link': i.siblings().eq(0)('a').attr('href'),
            'reply_count': '0' + i.siblings().eq(1).text(),
            'time': i.siblings().eq(2).text()
        } for i in doc('td.title').items()]
        print('finish:' + group_post_url)
        time.sleep(2)
    return post_list


def get_comment(post_url):
    # post_url = group_base_url + 'topic/%s/' % post_id
    doc = pq(post_url, headers=spider_header)
    reply_list = [{
        'username': li('h4>a').text(),
        'user_link': li('h4>a').attr('href'),
        'time': li('h4>span').text(),
        'content': li('p.reply-content').text()
    } for li in doc('ul#comments>li').items()]
    return reply_list


def get_comment_user_list(post_url):
    reply_list = get_comment(post_url)
    user_list = []
    for i in reply_list:
        user_info = i['username'] + ':' + i['user_link']
        if user_info not in user_list:
            user_list.append(user_info)
    for u in user_list:
        print(u)



member_group_id = '700330'  # 696739
search_group_id = '707438'  # 另一个爱乐之程692811,小浪组696121,大浪组689431
# temp_user_list = ['https://www.douban.com/people/223053663/', 'https://www.douban.com/people/223430215/']


def get_user_posts():
    with open('member-%s.txt' % member_group_id, 'r', encoding='utf-8') as f:
        member_list = [i.strip() for i in f.readlines()]
        posts = get_group_posts(search_group_id)
        for p in posts:
            if p['author_link'] in member_list:
                print('%s(%s): %s %s' % (p['author'], p['author_link'], p['title'], p['link']))


def get_user_comments():
    with open('member-%s.txt' % member_group_id, 'r', encoding='utf-8') as f:
        member_list = [i.strip() for i in f.readlines()]
        posts = get_group_posts(search_group_id)
        for p in posts:
            time.sleep(1)
            print('finish post: ' + p['link'])
            # if int(p['reply_count']) < 100:
            comments = get_comment(p['link'])
            for c in comments:
                if c['user_link'] in member_list:
                    print('%s(%s)' % (p['title'], p['link']))
                    print('%s(%s): %s %s\n' % (c['username'], c['user_link'], c['content'], c['time']))


if __name__ == '__main__':
    # get_user_posts()
    # get_user_comments()
    # get_group_posts(search_group_id)
    get_comment_user_list('https://www.douban.com/group/topic/198348651/')
