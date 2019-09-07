from bs4 import BeautifulSoup
from urllib.request import urlopen

url_base = 'https://qwer.gg'
url_team = '/teams'
teams = ['SKT/SK-Telecom-T1']

url = url_base + url_team + teams[0]
html = urlopen(url)
soup = BeautifulSoup(html, "html.parser")
soup