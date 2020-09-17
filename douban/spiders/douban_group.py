# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery as pq
spider_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.117 Safari/537.36'}

class DoubanGroupMemberSpider(scrapy.Spider):
    name = 'douban_group'
    group_id = '700330'
    allowed_domains = ['douban.com']
    # start_urls = ['https://www.douban.com/group/696739/members?start=' + str(i) for i in range(0, 13377, 35)]
    start_urls = ['https://www.douban.com/group/700330/members?start=' + str(i) for i in range(0, 5702, 35)]
    member_name_list = []
    member_link_list = []

    def parse(self, response):
        doc = pq(response.body)
        for i in doc('.name').items():
            name = i('a').text()
            link = i('a').attr("href") + '\n'
            self.member_name_list.append(name)
            self.member_link_list.append(link)

    @staticmethod
    def close(spider, reason):
        print('closed')
        with open('member-700330.txt', 'w+', encoding='utf-8') as f:
            f.writelines(list(set(spider.member_link_list)))
        return super().close(spider, reason)
