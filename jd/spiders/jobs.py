# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import re
from jd.items import JdItem
import csv
cn = 0
def mkdir(path):
    import os
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        print(path + ' 目录已存在')
        return False


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['shixiseng.com']
    params = {
        'k': 'Java',
        'p': 1
    }
    PAGES = 8
    FolderName = 'Shixiseng'
    base_url = "https://www.shixiseng.com/interns/st-intern_?"

    def __init__(self):
        mkdir(self.FolderName)
        self.out = open("Shixiseng/JnJd.csv", 'a+', newline='', encoding='utf-8')

        self.positions = dict()
        with open('test.csv', mode='r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            l = list(zip(reader))
            for i in l:
                d = {i[0][0]: i[0][3]}
                self.positions.update(d)
        print(self.positions)

    def start_requests(self):
        for i in range(self.PAGES):
            for j in self.positions:
                self.params['p'] = i+1
                self.params['k'] = self.positions[j]
                url = self.base_url + urlencode(self.params)
                yield Request(url=url, callback=self.parse, meta={'cate': j})

    def parse(self, response):
        r = BeautifulSoup(response.text, 'lxml')
        data = r.find_all(class_="position-name")
        for item_data in data:
            url = "https://www.shixiseng.com"+item_data['href']
            yield Request(url=url, callback=self.parse_item, meta=response.meta)

    def parse_item(self, response):
        res = response
        c = response.meta
        item = JdItem()
        bs4_response = BeautifulSoup(
            res.text.encode('gbk', 'ignore').decode('gbk', errors='ignore').replace('&nbsp;', ''), 'lxml')
        jd = bs4_response.find("div", {"class": "job_part"}).find("div", {"class": "job_detail"}).get_text()
        jd = re.sub('\n+', '\n', jd, re.S).strip("\n").strip()
        try:
            r = c['cate']
            mkdir(self.FolderName + '/' + r)
            item['jd'] = re.sub('\s+', '', jd, re.S)
            item['job_title'] = bs4_response.find("div", {"class": "new_job_name"}).get_text().strip()
            #print(item['jd'])
            global cn
            cn += 1
            print(cn)

            path = str(r) + '/' + str(cn) + '.txt'
            with open(self.FolderName + '/' + str(r) + '/' + str(cn) + '.txt', 'a', encoding="utf-8") as fw:
                fw.write(item['jd'])
            fw.close()
            print(item['jd'])
            JT = [item['job_title'], path]
            csv_writer = csv.writer(self.out, dialect='excel')
            csv_writer.writerow(JT)
            '''
            with open(str(cn) + '.txt', 'a', encoding='utf-8') as fwe:
                fwe.write(item['jd'])
            '''
            if '@' in item['jd']:
                with open(str(cn) + '.txt', 'a', encoding='utf-8') as fwe:
                    fwe.write(item['jd'])
            yield item
        except:
            print('职位爬取失败。。')
            print('失败页数：', self.PAGES)
