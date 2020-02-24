import requests
import re

class DoubanTop250Spider():

    def __init__(self):
        self.url = "https://movie.douban.com/top250?start={}"
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

    def getHtml(self,url):
	''' 获取目标url的response'''
        res = requests.get(url,headers=self.headers)
        html = res.text
        return html

    def getData(self,html):
	'''用正则提取出需要的数据'''
        pattern = re.compile(r'<li>(.*?)</li>',re.S)
        datas = pattern.findall(html)
        for data in datas[1:]:
            num = re.compile(r'<em class="">(.*?)</em>').findall(data)[0]
            title = re.compile(r'<span class="title">(.*?)</span>').findall(data)[0]
            rate = re.compile(r'<span class="rating_num".*?>(.*?)</span>').findall(data)[0]
            people = re.compile(r'<span>(.*?)</span>').findall(data)[0]
            movie_data = ("{}:{},{},{}".format(num,title,rate,people))
            self.saveData(movie_data)


    def saveData(self,movie_data):
	'''存储到txt文本中'''
        with open("doubanMovie.txt",'a') as f:
            f.write(movie_data+"\n")


    def workOn(self):
	'''主函数'''
        for pn in range(10):
            url = self.url.format(pn* 25)
            html = self.getHtml(url)
            data = self.getData(html)
            print('=======第{}页存储完成========'.format(pn+1))

if __name__ == "__main__":
    spider = DoubanTop250Spider()
    spider.workOn()