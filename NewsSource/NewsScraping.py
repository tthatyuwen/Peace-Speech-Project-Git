import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from newspaper import fulltext
import os
import asyncio
import aiohttp
import random
from lxml import html
import time
from datetime import date,timedelta
import base64
import re
from dateutil.relativedelta import relativedelta

Month_to_Num={
    'January':1,
    'February':2,
    'March':3,
    'April':4,
    'May':5,
    'June':6,
    'July':7,
    'August':8,
    'September':9,
    'October':10,
    'November':11,
    'December':12
}

# headers={
#     'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
# }

def webdriver_get_text(article_url_list):           # Use webdriver to get text(avoid AJAX)
    driver = set_driver()
    news_dict={}
    for url in article_url_list:
        try:
            driver.get(url)
            text = driver.page_source
            news_dict[url] = fulltext(text)
        except:
            print(f'{url} may have no content')
            continue
        time.sleep(5)
    return news_dict

def get_text(article_url_list):                               # use aiohttp and request to get text,perhaps faster
    async def get_source(url):
        async with aiohttp.ClientSession() as session:
            async with await session.get(url,headers=headers,timeout=10) as response:
                text = await response.text()
                try:
                    news_dict[url] = fulltext(text)
                except:
                    print(f'{url} may have no content')

    news_dict = {}

    if len(article_url_list)>0:
        iteration = len(article_url_list)//30
        for i in range(iteration+1):
            tasks = []
            sub_url_list = article_url_list[i*30:i*30+29]
            if len(sub_url_list) == 0:
                break
            for url in sub_url_list:
                tasks.append(get_source(url))
            asyncio.run(asyncio.wait(tasks))
            time.sleep(2)

    return news_dict

def save_text(news_dict,date,country):
    if len(news_dict)>0:
        path = './'+country+'_news'
        if os.path.exists(path):
            pass
        else:
            os.mkdir('./'+country+'_news')
        with open(path+f'/{date.year}-{date.month}-{date.day}.json','w') as f:
            json.dump(news_dict,f)

def set_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def get_url(driver,param,max_article):
    url, list_path, detailed_path = param['url'],param['list_path'],param['detailed_path']
    article_url_list=[]
    driver.get(url)
    page_text = driver.page_source
    tree = html.etree.HTML(page_text)
    li_list = tree.xpath(list_path)
    for li in li_list:
        try:
            if li.xpath(detailed_path)[0][:4]=='http':
                article_url = li.xpath(detailed_path)[0]
            else:
                title_break = url.split('/')
                if li.xpath(detailed_path)[0][0] == '/':
                    article_url = title_break[0] + '//' + title_break[2] + li.xpath(detailed_path)[0]
                else:
                    article_url = title_break[0]+'//'+title_break[2]+'/'+li.xpath(detailed_path)[0]
            article_url_list.append(article_url)
        except:
            print('Can not fetch url')
            pass
    if len(article_url_list)>max_article:
        article_url_list = random.sample(article_url_list, max_article)
    return article_url_list

def get_country_param(country,startdate,page=1):          # setting for different websites
    timestamp = (startdate - date(1900, 1, 1)).days + 2
    year, month, day = startdate.year, startdate.month, startdate.day
    params = {
        'India': {
            'url' : f'https://timesofindia.indiatimes.com/{year}/{month}/{day}/archivelist/year-{year},month-{month},starttime-{timestamp}.cms',
            'list_path' : '//tbody/tr[2]/td[1]/div[3]/table/tbody/tr[2]//a',
            'detailed_path' : './@href'},
        'Iran': {
            'url': f'https://www.tehrantimes.com/page/archive.xhtml?date={year}-{month}-{day}',
            'list_path': '//*[@id="mainbody"]//div[@class="third-news"]/ul/li',
            'detailed_path': './a/@href'},
        'Finland': {
            'url': f'https://www.dailyfinland.fi/archive/online-edition/{year}/{month}/{day}',
            'list_path': '//div[@id="archive_content_block"]//li',
            'detailed_path': './a/@href'},
        'Ireland': {  #2022.10.6-2020.1.1
            'url': f'https://www.sundayworld.com/archive/cnt/{year}/{month}/{day}',
            'list_path': '//main[@role="main"]//ul/li',
            'detailed_path': './a/@href'},
        'Nigeria': {
            'url': f'https://www.thenigerianvoice.com/archive/?sdate={str(base64.b64encode(startdate.strftime("%m/%d/%Y").encode("ascii")))[2:-1]}',
            'list_path': '//div[@id="contentbullet"]//li',
            'detailed_path': './a/@href'},
        'Norway': {
            'url': f'https://www.newsinenglish.no/{year}/{month}/{day}',
            'list_path': '//*[@class="vc_column tdi_62  wpb_column vc_column_container tdc-column td-pb-span8"]//h3[@class="entry-title td-module-title"]',
            'detailed_path': './a/@href'},
        'Uganda': {
            'url': f'https://www.independent.co.ug/all-news/page/{page}',
            'list_path': '//div[@id="main-content"]//div[@class="post-listing archive-box"]//h2[@class="post-box-title"]',
            'detailed_path': './a/@href'},
        "Sri_Lanka":{
            'url':f'https://www.sundaytimes.lk/'+startdate.strftime("%Y%m%d")[2:],
            'list_path':'//div[@id="subfeatured"]//h2',
            'detailed_path':"./a/@href"},
        "UK":{
            'url':f'https://www.independent.co.uk/archive/{year}-{startdate.strftime("%m")}-{startdate.strftime("%d")}',
            'list_path':'//*[@id="frameInner"]//li',
            'detailed_path':"./a/@href"},
        "Canada":{
            'url':f'https://www.thestar.com/archive/{year}/{startdate.strftime("%m")}/{startdate.strftime("%d")}.html',
            'list_path':'//*[@class="story-list"]//li',
            'detailed_path':"./a/@href"},
        "Zimbabwe":{
            'url' : f'https://bulawayo24.com/index-id-archive-yr-{year}-mnth-{month}.html',
            'list_path':'//*[@class="archive_mnth"]/li',
            'detailed_path':"./a/@href"},
        "Turkey":{
            'url':f'https://www.dailysabah.com/search?query=ARCHIVES&qlimit=by_fifty&pgno={page}',
            'list_path': '//*[@class="items_list"]//*[@class="widget_content"]/h3',
            'detailed_path':"./a/@href"},
        "Libya":{
            'url': f'https://www.libyaobserver.ly/archive/{year}{startdate.strftime("%m")}?page={page}',
            'list_path': '//*[ @ id = "block-system-main"]//ul[@class="links inline"]/li',
            'detailed_path': "./a/@href"
        },
        "Pakistan":{
            'url':f'https://www.dawn.com/archive/latest-news/{year}-{startdate.strftime("%m")}-{startdate.strftime("%d")}',
            'list_path': '/html/body/div[2]/div/div/div/div/div[2]/div/div/article',
            'detailed_path': "./h2/a/@href"
        },
        "France":{
            'url':f'https://www.france24.com/en/archives/{year}/{startdate.strftime("%m")}/{startdate.strftime("%d")}-{list(Month_to_Num.keys())[month-1]}-{year}',
            'list_path': '//ul[@class="o-archive-day__list"]//li',
            'detailed_path': "./a/@href"
        },
        "Gambia":{
            'url':f'https://thepoint.gm/africa/gambia/article?start={page}',
            'list_path': '//div[@class="row articles"]//h5',
            'detailed_path': "./a/@href"
        }
        }
    return params[country]

def main(country,startdate,setting_params={},max_article=30):
    if len(setting_params)==0:
        setting_params = get_country_param(country,startdate)
    article_url_list = get_url(set_driver(), setting_params,max_article)
    if country =='Nigeria':
        article_url_list = ['https://www.thenigerianvoice.com/amp'+url.split('com')[-1] for url in article_url_list]
    if country in ['Nigeria','Sri_Lanka',"Pakistan"]:
        news_dict = webdriver_get_text(article_url_list)
    else:
        news_dict = get_text(article_url_list)
    save_text(news_dict, startdate, country)

def Uganda_news(page):
    article_url_list = get_url(set_driver(), get_country_param('Uganda',date.today(),page),max_article=30)
    driver = set_driver()
    folder_path = './Uganda_news'
    if os.path.exists(folder_path):
        pass
    else:
        os.mkdir('./Uganda_news')
    for url in article_url_list:
        try:
            news_dict = {}
            driver.get(url)
            text = driver.page_source
            news_date = re.split('\W|,',html.etree.HTML(text).xpath('//span[@class="tie-date"]/text()')[0])
            news_date = f'{news_date[-1]}-{Month_to_Num[news_date[0]]}-{news_date[1]}'
            news = fulltext(text)
            path=f'./Uganda_news/{news_date}.json'
            f = open(path,'a+')
            try:
                news_dict = json.load(f)
            except:
                pass
            news_dict[url] = news
            json.dump(news_dict,f)
            f.close()
        except:
            print(f'{url} may have no content')
            continue

if __name__ == '__main__':

    # Example for using main/Uganda_news function
    # main('India',date(2022, 10, 6))
    # main('Iran', date(2022, 10, 6))
    # main('Finland', date(2022, 10, 6))
    # main('Ireland', date(2022, 10, 6))
    # main('Norway', date(2022, 10, 6))
    # main('Nigeria', date(2022, 10, 6))
    # main('UK', date(2022, 10, 6))
    # main('Canada', date(2022, 10, 6))
    # Uganda_news(1)
    # main('Sri_Lanka', date(2022, 10, 2))
    # main('Zimbabwe', startdate, max_article=1200)
    # main('Turkey',startdate,setting_params=get_country_param('Turkey',startdate,page=page),max_article=50)
    # main('Libya', startdate, setting_params=get_country_param('Libya', startdate, page=page), max_article=30)
    # main('France', startdate, max_article=30)
    # main('Pakistan', startdate, max_article=30)

    startdate = date(2018,12,31)
    while True:
        main('Nigeria', startdate, max_article=10)
        startdate -= timedelta(1)