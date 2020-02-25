import requests
from bs4 import BeautifulSoup
import urllib
import time
import pymongo

class DoubanbookSpider():

    def __init__(self):
	#��ǩ��url
        self.tag_url = 'https://book.douban.com/tag/?view=cloud'
	#�򿪱�ǩ��ÿһҳ��url
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
            #��һЩ��������������10�ˣ����Ծ�û������
            if rate == None:
                rate = '��'
            else:
                rate = rate.text
            people = data.find('span',class_='pl').text.replace(' ','').replace('\n','')
            tag_data.insert_one({'����':title,'����':pub,'����':rate,'��������':people})
            print('�Ѵ洢��{}��'.format(title))

    #���������б�ǩ
    def praseTaghtml(self,html):
        soup = BeautifulSoup(html,'lxml')
        all_tag = soup.find('table',class_='tagCol').find_all('a')
        for tag in all_tag:
            tag = tag.text
            #��ÿһ����ǩ����self.tags���list��
            self.tags.append(tag)

    def workOn(self):
        #��forѭ����ѭ��������ǩ�µ�ÿһҳ
        tag_html = self.getHtml(self.tag_url)
        self.praseTaghtml(tag_html)
        for tag in self.tags:
            tag_data = self.db['{}'.format(tag)]
            print('������ȡ��{}����ǩ'.format(tag))
            #������ת������ַ����ַ���
            tag = urllib.parse.quote(tag)
			#ÿһ����ǩֻ��ǰ50ҳ��ͼ����Ϣ�����Ǹ�ȡ�ɵİ취������ʡ��
            for page in range(1,51):
                print('======������ȡ��{}ҳ======'.format(page))
                pn = (page-1)*20
                url = self.page_url.format(tag,pn)
                print(url)
                html = self.getHtml(url)
                self.parsePagehtml(html,tag_data)
                time.sleep(1)

if __name__ == "__main__":
    spider = DoubanbookSpider()
    spider.workOn()