import feedparser

weibo_base_url = 'https://sister-rss.herokuapp.com/weibo/user/'
weibo_list = ['1839963312',  # 葵
              '1281047653',  # 0
              '1757744065',  # blue win win
              '2107123611',  # lsdn
              '1802626467',  # Jia
              '1821525001',  # Fei
              ]
ins_base_url = 'https://sister-rss.herokuapp.com/picuki/profile/'
ins_list = [
    'dream_613'
    'mjbaby0203',
    'ff0427',
    'jingsmusic',
    'yumiko.chengy',
    'yisayu1023'
]

def parse_weibo():
    result_list = []
    for account in weibo_list:
        result = feedparser.parse(weibo_base_url + account)
        for i in result['entries']:
            # print(i.keys())
            if 'vlo' in i['title']:
                result_list.append({
                    'title': i['title'],
                    'content': i['summary']
                })
    return result_list

def parse_ins():
    # for account in ins_list:
    result = feedparser.parse(ins_base_url + ins_list[2] + '?mode=fulltext')
    for i in result['entries'][0:1]:
        # print(i.keys())
        print(i['title'])
        print(i['summary'])
        print(i['published'])
        # print(i['published_parsed']) # 解析过的时间
        # print(i['id'])
        # print(i['guidislink'])
        print(i['links'])
        print(i['link'])
        # print(i['authors'])
        print(i['author'])

if __name__ == '__main__':
    parse_ins()
