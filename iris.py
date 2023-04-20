from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

url = 'https://www.iris.go.kr/contents/retrieveBsnsAncmBtinSituListView.do'
response = requests.get(url)
if response.status_code == 200:
    try:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        ul = soup.select_one('ul.dbody')
        titles = ul.select('li > div > div > strong')
        for title in titles:
            print(title.get_text())
            # print(go_url)
        exit()

        for link in soup.find("div", {'class': 'tstyle list biz_announce'}):
    
            print(link.text.strip())
    except Exception as error:
        print(error)