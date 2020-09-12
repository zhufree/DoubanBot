import feedparser

weibo_base_url = 'https://sister-rss.herokuapp.com/weibo/user/'
weibo_list = ['1839963312',  # 葵
              '1281047653',  # 0
              '1757744065',  # blue win win
              '2107123611',  # lsdn
              '1802626467',  # Jia
              '1821525001',  # Fei
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


if __name__ == '__main__':
    parse_weibo()
