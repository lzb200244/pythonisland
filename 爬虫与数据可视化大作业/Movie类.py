import asyncio
from urllib.parse import urljoin
import aiohttp
import requests
from lxml import etree
import time


def timer(func):
    def inner(*arg, **kwargs):
        s1 = time.time()
        func(*arg, **kwargs)
        print(f"消耗总时间:{time.time() - s1}")

    return inner


#

class Movie(object):
    datas = []
    lst = []

    def __init__(self):
        # global
        pass

    def get_detail(self):
        url = None
        try:
            for i in range(6):
                url = 'https://www.bpzhe.com/movie/%s/?zclass=华语' % i
                req = requests.get(url)
                tree = etree.HTML(req.text)
                div_lst = tree.xpath('//*[@id="archive-content"]/article')
                for div in div_lst:
                    yield div.xpath('./div[1]/a/@href')
        except:
            print(f"请求超时:{url}")

    async def task(self):
        tasks = []
        for url in self.get_detail():
            url = urljoin("https://www.bpzhe.com/", "".join(url))
            tasks.append(asyncio.create_task(self.get_info(url)))
        await asyncio.wait(tasks)

    async def get_info(self, url):
        try:
            async with aiohttp.ClientSession(headers={
                'User-Agen': '"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"'}) as session:
                async with session.get(url) as req:
                    content = await req.text()
                    tree = etree.HTML(content)
                    pat = '//*[@id="single"]/div[1]/div[1]/div[2]'
                    name = tree.xpath(f'{pat}/h1/text()')
                    type_ = tree.xpath(f'{pat}/div[4]/a[1]/text() | {pat}/div[4]/a[2]/text()')
                    if len(type_) == 2:
                        type_ = type_[0] + "/" + type_[1]
                    else:
                        type_ = type_[0]
                    comment = tree.xpath(f'{pat}/div[3]/div/div/div[2]/text()')
                    self.datas.append([name[0], type_, comment[0]])

        except Exception as e:
            print(f"请求超时:{e}")

    def save_data(self):
        lst = self.datas
        file = open("电影分析.csv", "a", encoding="utf8")
        for item in lst:
            for i in item:
                file.write(i)
                file.write(",")
            file.write("\n")
        file.close()


if __name__ == '__main__':
    print("我是Movie类")
