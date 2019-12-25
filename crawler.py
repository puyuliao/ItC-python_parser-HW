# -*- coding: utf-8 -*-
import requests
from lxml import etree
import time
import datetime

class Crawler(object):
    def __init__(self):
        self.req_str = 'https://www.csie.ntu.edu.tw/news/news.php?class=101&no=%d'
        self.base_url = 'https://www.csie.ntu.edu.tw/app/'
        self.last_date = '2012-07-09' #'2012-07-09' 
        self.date_xpath = '//*[@id="RSS_Table_page_news_1"]/tbody/tr[%d]/td[1]/text()'
        self.title_xpath = '//*[@id="RSS_Table_page_news_1"]/tbody/tr[%d]/td[2]/a/text()'
        self.href_xpath = '//*[@id="RSS_Table_page_news_1"]/tbody/tr[%d]/td[2]/a/@href'
        self.dt_last_date = datetime.datetime.strptime(self.last_date,'%Y-%m-%d')    
        self.content_xpath = '//*[@id="content2"]/div[2]//text()'
    def crawl(self, lowerdate, upperdate): 
        """upperdate(ex.2019-1-1) > lowerdate(ex.2018-12-23)"""
        """Main crawl API
            1. Note that you need to sleep 0.1 seconds for any request.
            2. It is welcome to modify TA's template.
        """
        """
        Parameters:
            start_date (datetime): the start date (included)
            end_date (datetime): the end date (included)
        Returns:
            content (list): a list of date, title, and content
        """
        res = []
        #dt_date1 = datetime.datetime.strptime(upperdate,'%Y-%m-%d')
        #dt_date2 = datetime.datetime.strptime(lowerdate,'%Y-%m-%d')
        # datetime.datetime has already converted in arg.py
        dt_date1 = upperdate
        dt_date2 = lowerdate
        for i in range (0,4000,10):
            time.sleep(0.1) # 10 times per sec
            """
            # TODO: parse the response and get dates (date), titles (title) and relative (href) url with etree
            """
            response = requests.get(self.req_str%(i),
                                    headers={'Accept-Language':
                                        'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6'})
            #print(i, response.status_code) # success = 200
            html_text = response.content.decode()
            root = etree.HTML(html_text)
            """Parse ten rows of the given page"""
            for j in range(1,11):
                date = root.xpath(self.date_xpath%(j))
                title = root.xpath(self.title_xpath%(j))
                href = root.xpath(self.href_xpath%(j))
                """
                # TODO: 1. concatenate relative url to full url
                #       2. for each url call self.crawl_content
                #          to crawl the content
                #       3. append the date, title and content to contents (res)
                """
                dt_date = datetime.datetime.strptime(date[0],'%Y-%m-%d')
                if dt_date1 >= dt_date and dt_date >= dt_date2:
                    obj = [date[0],title[0],self.crawl_content(self.base_url+href[0])]
                    res.append(obj)
                if dt_date <= self.dt_last_date: break
            if dt_date <= self.dt_last_date: break
        return res
    def crawl_content(self, url):
        """Crawl the content of given url
        For example, if the url is
        https://www.csie.ntu.edu.tw/news/news.php?Sn=15216
        then you are to crawl contents of
        ``Title : 我與DeepMind的A.I.研究之路,  ........ 現為DeepMind Staff Research Scientist。``
        """
        #print(url)
        time.sleep(0.1) # 10 times per sec
        response = requests.get(url)
        html_text = response.content.decode()
        root = etree.HTML(html_text)
        content = root.xpath(self.content_xpath)
        #print(content)
        res = ''.join(content)
        #print(type(res)
        return res.replace('\xa0','').replace('\r',' ').replace('\n','').replace('\"','\"').replace('\'','\'')
    #raise NotImplementedError
if __name__ == '__main__':
    cc = Crawler()
    #print(cc.crawl_content('https://www.csie.ntu.edu.tw/app/news.php?Sn=15216'))
    
    dt_date1 = datetime.datetime.strptime('2019-06-04','%Y-%m-%d')
    dt_date2 = datetime.datetime.strptime('2019-03-04','%Y-%m-%d')
    res = cc.crawl(dt_date1,dt_date2)
    for ele in res:
        print(ele)
    #print(res[0][2])
    
