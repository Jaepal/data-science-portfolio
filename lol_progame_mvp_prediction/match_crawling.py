from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from itertools import product
import pandas as pd
import re

# 크롤링 사이트 url
url_base = 'https://lol.gamepedia.com'
region_list_2018 = ['/NA_LCS', '/EU_LCS', '/LCK', '/LPL']
region_list_2019 = ['/LCS', '/LEC', '/LCK']
year_list_2018 = ['/2018_Season']
year_list_2019 = ['/2019_Season']
season_list = ['/Spring_Season', '/Summer_Season']

url = []
match_link = []
mvp = []

# 가능한 모든 url 조합 생성
url_detail_list_2018 = list(product(region_list_2018, year_list_2018, season_list))
url_detail_list_2019 = list(product(region_list_2019, year_list_2019, season_list))
url_detail_list = url_detail_list_2018 + url_detail_list_2019

for url_detail in url_detail_list:
    url.append(url_base + ''.join(url_detail))

# selenium
driver = webdriver.Chrome('./desktop/dataset/driver/chromedriver')

# 리스트에 각 매치 정보 링크를 저장하는 함수 생성
page = url[4]
def collect_match_links(url_list):
    for n, page in enumerate(url_list):
        print('[crawling... ', n+1, '/', len(url_list), ']')
        # url 페이지 접속
        driver.get(page)
        
        # 매치 테이블 상세 보기 클릭
        match_table = driver.find_element_by_xpath('//*[@id="md-table"]/tbody/tr[1]/th/div/div/span[1]')
        match_table.click()
        
        # 페이지 html 저장
        html = driver.page_source
        
        # BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        len(soup.find('table',{"id":"md-table"}).find_all('a', href=re.compile("^https://ma")))
        # 매치 링크 저장
        #match_link_raw = soup.find_all('a')
        match_link_raw = soup.find('table',{"id":"md-table"}).find_all('a', href=re.compile("^https?://ma"))
        for link in match_link_raw:
            match_link.append(link.attrs['href'])
        print(url_detail_list[n], len(match_link_raw), 'links saved')
        
        # MVP 저장

collect_match_links(url[8:])