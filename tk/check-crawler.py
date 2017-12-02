import requests
from bs4 import BeautifulSoup
url = 'http://www.cwb.gov.tw/V7/observe/real/ObsN.htm'
resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'lxml')

tp =  soup.select('table#63 > tr > td.temp1')[1].get_text()
print tp
