
from pyspider.libs.base_handler import *
import os

PAGE_START = 1
PAGE_END = 5
DIR_PATH = '/Users/zhangning/Desktop/taobaomm/'


class Handle(BaseHandler):

    crawl_config = {

    }

    def __init__(self):
        self.base_url = 'https://mm.taobao.com/json/request_top_list.htm?page='
        self.page_num = 1
        self.total_num = 30
        self.deal = Deal()

    @every(minutes=24 * 60)
    def on_start(self):
        while self.page_num < self.total_num:
            url = self.base_url + str(self.page_num)
            print(url)
            self.crawl(url, callback=self.index_page)
            self.page_num += 1

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.lady-name').items():
            self.crawl(each.attr.href, callback=self.detail_page, fetch_type='js')

    @config(priority=2)
    def detail_page(self, response):
        domain = 'https:' + response.doc('.mm-p-domain-info li > span').text()
        print domain
        self.crawl(domain, callback=self.domain_page)

    def domain_page(self, response):
        name = response.doc('.mm-p-model-info-left-top dd > a').text()
        dir_path = self.deal.mk_dir(name)
        brief = response.doc('.mm-aixiu-content').text()
        if dir_path:
            imgs = response.doc('.mm-aixiu-content img').items()
            count = 1
            self.deal.save_brief(brief, dir_path, name)
            for img in imgs:
                url = img.attr.src
                if url:
                    extension = self.deal.get_ext(url)
                    file_name = name + str(count) + '.' + extension
                    count += 1
                    self.crawl(url, callback = self.save_img, save={'dir_path': dir_path, 'file_name': file_name})

    def save_img(self, response):
        content = response.content
        dir_path = response.save['dir_path']
        file_name = response.save['file_name']
        file_path = dir_path + '/' + file_name
        self.deal.save_img(content, file_path)


class Deal:

    def __init__(self):
        self.path = DIR_PATH
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def mk_dir(self, path):
        path = path.strip()
        dir_path = self.path + path
        exists = os.path.exists(dir_path)
        if not exists:
            os.makedirs(dir_path)
        return dir_path

    def save_img(self, content, path):
        f = open(path, 'wb')
        f.write(content)
        f.close()

    def save_brief(self, content, path, name):
        file_name = path + '/' + name + ".txt"
        f = open(file_name, 'w+')
        f.write(content.encode('utf-8'))
        f.close()

    def get_ext(self, url):
        extension = url.split('.')[-1]
        return extension
