from selenium import webdriver
from bs4 import BeautifulSoup as bs
import csv 
import pandas as pd
from datetime import datetime

def get_hunjang(url,pg):
    # webdriver 객체 생성
    webdriver_path = 'chromedriver.exe 절대경로'
    driver = webdriver.Chrome(webdriver_path)
    # 페이지 접근
    driver.get(url)
    soup = bs(driver.page_source ,'html.parser')
    
    soup = soup.find(class_ = 's-adBn-wrap')#채용정보
    if pg <=1 :
        soup = soup.find_all(class_ = 'adRc-inner')[5] #1:스페셜, 2:포커스 3:플러스 4:리스트 5일반
    else:
        soup = soup.find_all(class_ = 'adRc-inner')[0] #두번째 페이지부터 변경

    table = soup.find('table', class_='retbl-col')
    rows = table.find_all('tr')
    
    datas_list=[]
    for idx,tr in enumerate(rows):
        result={}
        if idx>0:
            tds = tr.find_all('td')
            result['academy_name'] = tds[1].text.rstrip()
            result['title'] = tds[2].text.strip()
            result['local'] = tds[3].text.rstrip().split("\n")[1]
            result['subject']=tds[3].text.rstrip().split("\n")[2]
            
            result['start_date'] = tds[4].text
            result['end_date'] = tds[5].text
            datas_list.append(result)
                   
    return datas_list

def get_dataframe():
    df_fin = pd.DataFrame()
    for pg in range(1,31): # 09.13.23시기준 마지막페이지30
        url = "https://www.hunjang.com/adopt/adopt_total_list.asp?schSubject=01&schSubject_name=%B1%B9%BE%EE&schSubject=02&schSubject_name=%BF%B5%BE%EE&schSubject=03&schSubject_name=%BC%F6%C7%D0&nPage="+str(pg)+"&nPageSize=0&sort_order=&textkey=&textword="
        data_list = get_hunjang(url,pg)
        
        df = pd.DataFrame(data_list,columns=['academy_name','title','local','subject','start_date','end_date'])
        df_fin = pd.concat([df_fin,df],axis=0,ignore_index=True)
    return df_fin

df = get_dataframe()
#print(df.head())
today_date = datetime.today().strftime("%Y-%m-%d")
filename = today_date+'-hunjang_crawling.csv'  
df.to_csv('./Data/학원_Data/'+filename,encoding='utf-8-sig')
#print("csv저장성공! "+today_date)

# 문제점 : 실시간으로 데이터가 계속해서 늘어남, 현재 마지막페이지가 30인데 더 늘어날 수도 있음. 
# 해결방법 : 주기적으로 업데이트를 해서 변경된 부분만 가져와도록..