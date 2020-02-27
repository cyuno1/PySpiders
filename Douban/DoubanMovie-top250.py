import requests
import re
import random

class DoubanTop250Spider():

    def __init__(self):
        self.url = "https://movie.douban.com/top250?start={}"
	
	def getHeaders(self):
	    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"]
		UA = random.choice(user_agent_list)
		headers = {'User-Agent':UA}
		return headers

    def getHtml(self,url):
	''' 获取目标url的response'''
        res = requests.get(url,headers=self.getHeaders())
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