import requests
from bs4 import BeautifulSoup
import urllib
import time
import pymongo

class DoubanbookSpider():

    def __init__(self):
	#标签的url
        self.tag_url = 'https://book.douban.com/tag/?view=cloud'
	#打开标签后每一页的url
        self.page_url = 'https://book.douban.com/tag/{}?start={}&type=T'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        self.tags = []
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client['douban_book']


    def getHtml(self,url):
        response = requests.get(url,headers=self.headers)
        html = response.text
        return html

    def parsePagehtml(self,html,tag):
        soup = BeautifulSoup(html,'lxml')
        all_book = soup.find_all('div',class_='info')
        tag_data = tag
        for data in all_book:
            title = data.find('a').text.replace(' ','').replace('\n','')
            pub = data.find('div',class_='pub').text.replace(' ','').replace('\n','')
            rate = data.find('span',class_='rating_nums')
            #有一些书评价人数少于10人，所以就没有评分
            if rate == None:
                rate = '无'
            else:
                rate = rate.text
            people = data.find('span',class_='pl').text.replace(' ','').replace('\n','')
            tag_data.insert_one({'名称':title,'作者':pub,'评分':rate,'评价人数':people})
            print('已存储《{}》'.format(title))

    #解析出所有标签
    def praseTaghtml(self,html):
        soup = BeautifulSoup(html,'lxml')
        all_tag = soup.find('table',class_='tagCol').find_all('a')
        for tag in all_tag:
            tag = tag.text
            #把每一个标签放入self.tags这个list中
            self.tags.append(tag)

    def workOn(self):
        #用for循环，循环单个标签下的每一页
        tag_html = self.getHtml(self.tag_url)
        self.praseTaghtml(tag_html)
        for tag in self.tags:
            tag_data = self.db['{}'.format(tag)]
            print('正在爬取【{}】标签'.format(tag))
            #把中文转换成网址里的字符串
            tag = urllib.parse.quote(tag)
			#每一个标签只有前50页有图书信息，这是个取巧的办法，但是省事
            for page in range(1,51):
                print('======正在爬取第{}页======'.format(page))
                pn = (page-1)*20
                url = self.page_url.format(tag,pn)
                print(url)
                html = self.getHtml(url)
                self.parsePagehtml(html,tag_data)
                time.sleep(1)

if __name__ == "__main__":
    spider = DoubanbookSpider()
    spider.workOn()