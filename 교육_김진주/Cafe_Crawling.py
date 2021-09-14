import requests
import json
import pandas as pd 
from datetime import datetime

import os
import sys

from selenium import webdriver
from bs4 import BeautifulSoup as bs

today_date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

def get_cafe_url(url):
    # webdriver 객체 생성

    # linux에서 사용할경우 chromedirver 다시 다운받고 새로운 경로 지정하기 
    driver = webdriver.Chrome(executable_path='./driver/chromedriver.exe')

    # 페이지 접근
    # 날짜지정, 검색어('과외추천')지정, 50개씩보이기
    #url = "https://cafe.naver.com/hikicks?iframe_url=/ArticleSearchList.nhn%3Fsearch.clubid=12946579%26search.media=0%26search.searchdate=2016-01-012021-09-13%26search.defaultValue=1%26search.exact=%26search.include=%26userDisplay=50%26search.exclude=%26search.option=0%26search.sortBy=date%26search.searchBy=1%26search.includeAll=%26search.query=%B0%FA%BF%DC%C3%DF%C3%B5%26search.viewtype=title%26search.page=1"
    driver.get(url)
    driver.switch_to.frame('cafe_main')

    soup = bs(driver.page_source ,'html.parser')
    soup = soup.find_all(class_ = 'article-board m-tcol-c')[1]# 네이버 카페 구조 확인후 게시글 내용만 가저오기

    datas_list=[]
    datas = soup.find_all(class_ = 'td_article')
    for data in datas:
        article_title = data.find(class_ = 'article')
        article_title = article_title.get_text().strip()
        datas_list.append(article_title)
    return datas_list

def save_data():
    keyword = "과외추천"
    #query=%B0%FA%BF%DC%C3%DF%C3%B5%26
    #url에 keyword값을 변경해서 파라미터로 넣도록

    df_fin = pd.DataFrame()
    for pg in range(1,45): #끝 페이지번호 44
        url = "https://cafe.naver.com/hikicks?iframe_url=/ArticleSearchList.nhn%3Fsearch.clubid=12946579%26search.media=0%26search.searchdate=2016-01-012021-09-13%26search.defaultValue=1%26userDisplay=50%26search.option=0%26search.sortBy=date%26search.searchBy=1%26search.query=%B0%FA%BF%DC%C3%DF%C3%B5%26search.viewtype=title%26search.page="+str(pg)
        data_list = get_cafe_url(url)
        
        df = pd.DataFrame(data_list)
        df_fin = pd.concat([df_fin,df],axis=0,ignore_index=True)

    filename = today_date+'./Data/학원_Data/cafe_crawling.csv'  
    df_fin.to_csv(filename,encoding='utf-8-sig')

save_data()