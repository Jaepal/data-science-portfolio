from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd

# 크롤링 사이트 url
url_base = 'https://qwer.gg'
url_teams = []
url_players = []
team_name = []

# selenium
driver = webdriver.Chrome('./desktop/dataset/driver/chromedriver')
driver.get(url_base)
driver.implicitly_wait(1.5)
html = driver.page_source

# BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

## 각 팀 url 수집
for link in soup.find_all('a', class_='LeagueTeams__link'):
    url_teams.append(link.attrs['href'])

## 각 팀 선수 이름 수집
for team in url_teams:
    print(team)
    url = url_base + str(team)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    for player in soup.find_all('a', class_='PlayerCard Team__players__item'):
        url_players.append(player['href'])
        team_name.append(team.split('/')[2])
    '''
    url_players = [player['href'] for player in soup.find_all('a', class_='PlayerCard Team__players__item')]
    '''

## 각 선수 스탯 수집

# 스탯을 담을 DataFrame 생성
stats = pd.DataFrame(columns=['Player', 'Season', 'Champion', 'Game', 'Win', 'Lose', 'WinRate', 'Kill', 'Death', 'Assist',
                              'KDA', 'VS', 'DMG', 'DPM', 'DTPM', 'CS', 'CSPM', 'KPAR', 'DPAR', 'KS', 'Gold', 'GPM', 'Base'])


# 출전 여부를 확인하는 함수 생성
def menu_check_exists_by_By():
    try:
        driver.find_element(By.CSS_SELECTOR, "div.TeamStats__menu")
    except NoSuchElementException:
        return False
    return True

def spring_check_exists_by_xpath():
    try:
        driver.find_element_by_xpath('''//*[@id="root"]/div[4]/div[2]/div/section/div/div[1]''')
    except NoSuchElementException:
        return False
    return True

def summer_check_exists_by_xpath():
    try:
        driver.find_element_by_xpath('''//*[@id="root"]/div[4]/div[2]/div/section/div/div[2]''')
    except NoSuchElementException:
        return False
    return True

for player in url_players:
    print(player.split('/')[2], '정보')
    url = url_base + str(player)
    driver.get(url)
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.TeamStats__menu")))
    except TimeoutException:
        print('출전하지 않음')
        continue
    
    # Spring, Summer 탭 위치 저장
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    spring, summer = 0, 0
    if menu_check_exists_by_By:
        menu = list(map(lambda a: a.text, soup.select('div.TeamStats__menu > div')))
        if '2019 LCK Spring' in menu:
            spring = menu.index('2019 LCK Spring') + 1
        if 'LCK 2019 Summer' in menu:
            summer = menu.index('LCK 2019 Summer') + 1
    else:
        continue
    
    # 스프링 데이터 저장
    if spring:
        # 스프링 테이블 클릭
        print('스프링 테이블 클릭')
        spring_raw = driver.find_element_by_xpath('//*[@id="root"]/div[4]/div[2]/div/section/div/div[' + str(spring) + ']')
        spring_raw.click()
        
        # 스프링 html 저장
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        # 챔피언 스탯을 담은 list 생성
        table = list(map(lambda a: a.text, soup.select('table.StatsTable > tbody > tr > td')))
        
        # 스프링 데이터를 DataFrame에 추가
        for idx in range(len(table)//21):
            stat = [player.split('/')[2], '2019 LCK Spring']
            stat.extend(table[idx*21:(idx+1)*21])
            stats.loc[len(stats),:] = stat
        print(player.split('/')[2], '스프링 데이터 추가 완료')

    else:
        print('스프링 출전하지 않음')
    
    # 서머 데이터 저장
    if summer:
        # 서머 테이블 클릭
        print('서머 테이블 클릭')
        summer_raw = driver.find_element_by_xpath('//*[@id="root"]/div[4]/div[2]/div/section/div/div[' + str(summer) + ']')
        summer_raw.click()
        
        # 서머 html 저장
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        # 스탯 list에 서머 데이터 추가
        table = list(map(lambda a: a.text, soup.select('table.StatsTable > tbody > tr > td')))
        
        # 스프링 데이터를 DataFrame에 추가
        for idx in range(len(table)//21):
            stat = [player.split('/')[2], '2019 LCK Summer']
            stat.extend(table[idx*21:(idx+1)*21])
            stats.loc[len(stats),:] = stat
        print(player.split('/')[2], '서머 데이터 추가 완료')
    else:
        print('서머 출전하지 않음')
