import requests
from pyquery import PyQuery as pq 
from urllib import parse 
import csv
import time
from selenium import webdriver
import mongo
import db 



class Spider(object):

    base_url = "http://weixin.sogou.com/weixin"    #基本url
    key_word = 'AI'   #搜搜关键词
    #list_url = []   #存储url和其callback 函数
    #list_item = []   #临时存储url和callback函数， 只存储两个数据，添加到list_url 后，应该立即清空
    #session = requests.Session()   #开始设置
    """
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'sw_uuid=3334394017; sg_uuid=2065896719; dt_ssuid=853760490; pex=C864C03270DED3DD8A06887A372DA219231FFAC25A9D64AE09E82AED12E416AC; ssuid=8258541632; CXID=33A866F87888D6C8D1A553B76F2BADCA; SUV=00C02729B46B344C5B72F4ADF43D0798; ad=Vyllllllll2bt0CzlllllVHCuHYlllllWWn@vlllll9lllll9Vxlw@@@@@@@@@@@; SUID=53DA31773765860A5B11413D000B34E8; pgv_pvi=431889408; ABTEST=0|1534575838|v1; weixinIndexVisited=1; SUIR=CBA7F587B6B0C605F48511D2B6DE9810; ld=cyllllllll2bNDvxlllllVHThntlllllGUlvKyllllGlllll9klll5@@@@@@@@@@; LSTMV=385%2C26; LCLKINT=3828; ppinf=5|1534577030|1535786630|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyOkJDfGNydDoxMDoxNTM0NTc3MDMwfHJlZm5pY2s6MjpCQ3x1c2VyaWQ6NDQ6bzl0Mmx1RkZDdlpaY1dsTmdsalgwYzd4dE1iY0B3ZWl4aW4uc29odS5jb218; pprdig=R6R352FfiGDW1H3tvcqyhorgCkT3odPRYTPZ6thnUHaWCcL8UwwFEC0W9gzyUhzku8ScAL6CKkabRXXTfE-0dh1--l0JtsESkg17NAfPWozGHDP-9Cvpu2Ptq3VSXL_WM0U0R_tAFMHYEKwu3nrfiziia6XaFgqf5RrLXJuDUa0; sgid=16-36640129-AVt3yYYDq8t3XJ2MTXx5PMc; SNUID=9A8F42F88286F68589E463E1837385F0; IPLOC=CN2200; JSESSIONID=aaafIZVUumv_l7fFtEBvw; pgv_si=s8715192320; ppmdig=1535095739000000e7ea71c241fae9486d10ed0a4333c9a9; sct=14',
        'DNT':'1',
        'Host':'weixin.sogou.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        }
    """
    cookies = {'sw_uuid':'3334394017', 
            'sg_uuid':'2065896719', 
            'dt_ssuid':'853760490', 
            'pex':'C864C03270DED3DD8A06887A372DA219231FFAC25A9D64AE09E82AED12E416AC', 
            'ssuid':'8258541632', 
            'CXID':'33A866F87888D6C8D1A553B76F2BADCA', 
            'SUV':'00C02729B46B344C5B72F4ADF43D0798',
            'ad':'Vyllllllll2bt0CzlllllVHCuHYlllllWWn@vlllll9lllll9Vxlw@@@@@@@@@@@', 
            'SUID':'53DA31773765860A5B11413D000B34E8', 
            'pgv_pvi':'431889408', 
            'ABTEST':'0|1534575838|v1', 
            'weixinIndexVisited':'1', 
            'ld':'cyllllllll2bNDvxlllllVHThntlllllGUlvKyllllGlllll9klll5@@@@@@@@@@', 
            'LSTMV':'385%2C26','LCLKINT':'3828','SNUID':'9A8F42F88286F68589E463E1837385F0', 
            'IPLOC':'CN2200', 
            'pgv_si': 's3126373376', 
            'sct':'17', 
            'JSESSIONID':'aaaYnzdJQDdUUguOHzBvw', 
            'ppinf':'5|1535195192|1536404792|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyOkJDfGNydDoxMDoxNTM1MTk1MTkyfHJlZm5pY2s6MjpCQ3x1c2VyaWQ6NDQ6bzl0Mmx1RkZDdlpaY1dsTmdsalgwYzd4dE1iY0B3ZWl4aW4uc29odS5jb218',
            'pprdig':'eUprT1c-kM2bGGGiLWMW1FXo7TtbFMefITQzQeMOrxkE4dDJgEM15cuAXV1rcjDAXQR4-eqOc7Ycf8F7GwrWUylY1QiEjvrz-cMiEyjtWWMWAf8fkG4G5ZHbMpk0HR14pjbMQZGjZlrS57ZDsIiv3l_uGA5SpI7dIflpnoMu-ok',
            'sgid':'16-36640129-AVuBODg3a8UkW2FdLzwf2W4', 
            'ppmdig':'1535195193000000ecfc6e6a5c33bb04d8a46936b64d2333'
            }


    csvfile = open("url.csv","a",encoding="utf-8", newline='')  
    
    writer = csv.writer(csvfile)
    
    browser = webdriver.Firefox()      #声明浏览器
    browser.get(base_url)

    #添加cookie
    for key, value in cookies.items():
        name = key
        value = value

        cookie = {
            'name':name,
            'value': value,
        }
        browser.add_cookie(cookie)

    mongo = mongo.Mongo()    #类的实例化
    redis = db.Redis()  #redis 的实例化

    def start(self):
        """
            初始化，用来初始list_item 和 list_url
        """
        #self.session.headers.update(self.headers)
        url = self.base_url + "?" + parse.urlencode({'type':'2',"query":self.key_word,}) 
        url_item = [url, self.parse_index]
        self.redis.push(url_item)

        #self.list_url.append(url_item)

    def parse_index(self, html):
        """
            用于解析每个页面的链接，返回的值为url 和 调度函数组成的列表
        """
        print("链接页")
        
        try:
            doc = pq(html)
            items = doc('.news-list h3 a').items()
            for item in items:
                url = item.attr['href'].replace("amp:","")
                self.writer.writerow([url])    #写入csv  
                url_item = [url, self.parse_detail]
                yield url_item

        except:
            print("url提取错误")

        doc = pq(html)
        next_page = doc("#sogou_next").attr['href']
        url =  self.base_url + str(next_page)
        url_item = [url, self.parse_index]
        yield url_item


    def parse_detail(self, html):
        """
            用于解析每页的文章的详细信息， 返回的信息为dic
        """
        print("详情页")
        try:
            doc = pq(html)
            data = {
                'title': doc('#activity-name').text(),
                'content': doc(".rich_media_content").text() 
            }
        except:
            print("文章内容提取出错")
        else:
            yield data

    def request(self, url):
        try:
            time.sleep(3)
            self.browser.get(url)
            time.sleep(5)
            sroll_cnt = 0
            while  True:
                if sroll_cnt < 5:
                    self.browser.execute_script('window.scrollBy(0, 1000)')
                    time.sleep(1)
                    sroll_cnt += 1
                else:
                    break

            html =self.browser.page_source          #获取网页源代码
        except:
            print("获取源代码错误")

        else:
            if len(html) != 0 :
                return html
            else:
                print("获取源代码错误")
                return html


    def scheduler(self):
        """
            用于调度程序
        """
        self.redis.delete()  #决定是否重新开始
        if self.redis.llen():   #列表长度为空，则完成初始化
            self.start()   
        while True:
            if not self.redis.llen():
                url_item = self.redis.pop() 
                url = url_item[0]
                callback = url_item[1]
                print("schedulering url:", url)
                html = self.request(url)
                for item in callback(html):
                    if isinstance(item, dict):
                        self.mongo.save(item)
                    elif isinstance(item, list):
                        self.redis.push(item) #存储到redis
            else:
                print("url队列已经空了！")
                break
    def run(self):
        self.scheduler()

if __name__ == '__main__':
    app = Spider()
    print("working")
    app.run()
    print("all was done!")