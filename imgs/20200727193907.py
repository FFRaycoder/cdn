from os import path, mkdir
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import urllib.request
import requests


class WallPaperAccessSpider:
    def __init__(self, url):
        self.wallpaper_url = url
        self.url_proto = 'https://' if self.wallpaper_url.startswith('https://') else 'http://'
        self.base_url = self.wallpaper_url.replace(self.url_proto, '')\
            .split('/')[0]
        self.imgs = []
        self.HEADERS = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://wallpaperaccess.com/',
            'User-Agent': UserAgent().random
        }

    def get_img_urls(self):
        html = BeautifulSoup(requests.get(self.wallpaper_url, headers = self.HEADERS).text, 'html.parser')
        for img in html.find_all('img', {'data-id': True, 'data-src': True}):
            self.imgs.append(self.url_proto + self.base_url + img['data-src'])

    def download(self, img_path):
        if not path.exists(img_path): mkdir(img_path)
        for each_img in self.imgs:
            img_name = each_img.split('/')[-1]
            urllib.request.urlretrieve(each_img, path.abspath(img_path + img_name))

def _main():
    spider = WallPaperAccessSpider('https://wallpaperaccess.com/4k-minimalist')
    spider.get_img_urls()
    spider.download('imgs/')

if __name__ == '__main__':
    _main()
