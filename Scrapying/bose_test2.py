# -*- coding: utf-8  -*-
# -*- author: jokker -*-
import time
import requests
from requests import Session
from http import client
import re
from lxml import etree
import json
import random


client._is_legal_header_name = re.compile(br':|\A[^:\s][^:\r\n]*\Z').match

class BossSpider():
    session = Session()
    num = 0
    company ={
        # 'zhifubao': '1f8227007663695b3nV63Q~~',
        # 'baidu': 'ab9fdc6f043679990HY~',
        'tenxun': '2e64a887a110ea9f1nRz',
        'ali': '5d627415a46b4a750nJ9',
        'zijietiaodong': 'a67b361452e384e71XV82N4~',
        'huawei':'02cd05cce753437e33V50w~~',
        'wangyi':'821662f4a993420c3nZ62dg~',
        # 'jindong':'755f9f2f1799f89a03d60g~~',
        # 'mayi':'e9a2427bc19f1b1a33Z_3t0~',
        # 'jdjituan':'33e052361693f8371nF-3d25',
        # 'BJzijie':'7d01ce6cfe2022030HJ409y-',
        # 'bjtenxun':'0979070fc97e501a0nx7'
        }
    USER_AGENT_LIST=[
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]


    def __init__(self):
        self.proxy = self.get_proxy()
        self.agent = random.choice(self.USER_AGENT_LIST)
        self.headers = {
        ':authority': 'www.zhipin.com',
        ':method': 'GET',
        # ':path': urlb,
        ':scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'cache-control': 'max-age=0',
        # 'referer': urla + '/{}/?page={}&ka=page-{}'.format(cp,page-1,page-1) if page>1 else 'https://www.zhipin.com/c101020100-p100109/',
        'user-agent': self.agent,
        }

    def get_proxy(self):
        url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=c0fc4a1f24e245dc85fd15c355fc3530&orderno=YZ20191237434d6v6Z&returnType=1&count=1'
        text = requests.get(url).text
        print('请求代理:',"http://"+text.strip())
        if '频繁' not in text:
            proxy = {
            'http':"http://"+text.strip(),
            'https':'https://'+text.strip()
            }
            self.proxy = proxy
        elif '10032' in text:
            print(text)
            print('代理用完')
            self.proxy = 'None'
        elif '频繁' in text:
            print('\n5秒后再获取代理\n')
            time.sleep(5.5)
            self.get_proxy()

    def get_detail(self,jid,lid):
        url = 'https://www.zhipin.com/view/job/card.json?jid={jid}&lid={lid}&type=2'.format(jid=jid,lid=lid)
        self.agent = random.choice(self.USER_AGENT_LIST)
        self.session.headers.update(self.headers)
        try:
            response = self.session.get(url, proxies=self.proxy, headers=self.headers, timeout=5)
            if '请求成功' in response.text:
                html = response.json()['html']
                return html
            elif self.proxy=='None':
                return None
            else:
                self.get_proxy()
                self.get_detail(self,jid,lid)
        except Exception as e:
            print('\n\n遇到错误',e)
            self.get_proxy()
            self.get_detail(jid,lid)

    def getpage(self, factor, page):
        self.agent = random.choice(self.USER_AGENT_LIST)
        self.session.headers.update(self.headers)
        url = 'https://www.zhipin.com/gongsir/{factor}.html?page={page}&ka=page-{page}'.format(factor=factor,page=page)
        try:
            response = self.session.get(url, proxies=self.proxy, timeout=5, headers=self.headers)
            html = response.text
            if '公司简介' in html:
                print('----------------获取{}列表页{}page\n'.format(factor,page))
                return html
            elif self.proxy=='None':
                return None
            elif '过于频繁' in html or '您的账号安全' in html:
                print('====过于频繁')
                self.get_proxy()
                self.getpage(factor, page)
        except:
            self.getpage(factor, page)


    def parse_detail(self, html):
        ''
        html = etree.HTML(html)
        text = html.xpath("//div[@class='detail-bottom']//text()")
        text = ''.join((s.strip() for s in text))
        if len(text)>20:
            print('\t\t解析到详情页',text[0:20])
        return text

    def parse_page(self, html):
        html = etree.HTML(html)
        lis = html.xpath("//div[@class='job-list']//li")
        for li in lis:
            title = li.xpath(".//h3[@class='name']//div[@class='job-title']//text()")[0] if len(li.xpath(".//h3[@class='name']//div[@class='job-title']//text()")) else None
            salary = li.xpath(".//h3[@class='name']//span[@class='red']//text()")[0] if len(li.xpath(".//h3[@class='name']//span[@class='red']//text()")) else None
            location = li.xpath(".//div[@class='info-primary']/p/text()")[0] if len(li.xpath(".//div[@class='info-primary']/p/text()"))>0 else None
            require = li.xpath(".//div[@class='info-primary']/p/text()")[1] if len(li.xpath(".//div[@class='info-primary']/p/text()"))>1 else None
            edu = li.xpath(".//div[@class='info-primary']/p/text()")[2] if len(li.xpath(".//div[@class='info-primary']/p/text()"))>2 else None
            company = html.xpath('//div[@class="info-primary"]/h1//text()')[0] if len(html.xpath('//div[@class="info-primary"]/h1//text()')) else None
            jid = li.xpath("./a/@data-jid")[0]
            lid = li.xpath("./a/@data-lid")[0]
            url = 'https://www.zhipin.com/'+li.xpath("./a/@href")[0] if len(li.xpath("./a/@href")) else None
            self.num += 1
            print('\t',self.num,'获得:'+title)
            detail_html = self.get_detail(lid=lid,jid=jid)
            if detail_html:
                infor = self.parse_detail(detail_html)

                if company is None:
                    company = str(random.random())

                with open('{0}boss.txt'.format(company[:2]),'a',encoding='utf-8',errors='replace') as f1:
                    f1.write('\t'.join(str(_) for _ in (title, salary, company, edu, location, require, infor, url)) + '\n')
                item ={
                'title': title,
                'salary': salary,
                'location': location,
                'require': require,
                'edu': edu,
                'company': company,
                'infor':infor,
                'url': url
                }
                with open('{}json.txt'.format(company[:2]),'a',errors='replace',encoding='utf-8') as f2:
                    f2.write(json.dumps(item,indent=4,ensure_ascii=False)+"\n")
            else:
                pass
    def update_company(self):
        f = open('company_url.txt','w',encoding='utf-8')
        for page in range(1,30):
            r = requests.get('https://www.zhipin.com/gongsi/?page={page}&ka=page-{page}'.format(page=page),headers=self.headers,proxies=self.proxy)
            html = etree.HTML(r.text)
            if '暂时没有' in r.text:
                break
            elif '过于频繁' in r.text:
                self.proxy=self.get_proxy()
                self.update_company()
            elif '精准匹配' in r.text:
                lis = html.xpath("//div[contains(@class,'company-tab-box') and contains(@class,'company-list')]//li")
                for li in lis:
                    com = li.xpath(".//div[@class='conpany-text']/h4/text()")
                    url = li.xpath(".//div[@class='sub-li']/a[1]/@href")
                    if com and url:
                        com=com[0]
                        url=url[0].replace('/gongsi/','').replace('.html','')
                        self.company[com]=url
                        f.write(com+'\t'+url+'\n')
        f.close()

    def load_company(self):
        with open('company_url.txt','r',encoding='utf-8') as f:
            companylist = f.readlines()
            for i in companylist:
                if i:
                    com = i.split("\t")[0]
                    url = i.split("\t")[1].strip()
                    self.company[com]=url

    def main(self):
        for key in self.company:
            if self.proxy=='None':
                break
            value=self.company[key]
            for page in range(1,31):
                if self.proxy=='None':
                    break
                html = self.getpage(value,page)
                time.sleep(1)
                if html:
                    self.parse_page(html)

if __name__ == '__main__':
    boss = BossSpider()
    boss.main()
