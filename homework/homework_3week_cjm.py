import requests
from bs4 import BeautifulSoup

# URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&ymd=20200403&hh=23&rtm=N&pg=1',headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

#문제 1위~50위의 곡에서 순위 제목 가수이름 순으로 스크래핑 하기

#body-content > div.newest-list > div > table > tbody
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis

#tbody불러오기
musics = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
#print(musics)
#for music in musics:
    # 1번은 되는데 전체값에서는 text가 안먹혀서 전체값을 불러오기가 안됌
    # musics = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
    # 여기서 tr 을 추가 안해줘서 1번만 적용되서 다 안나온것이였음..
    #rank = music.select('td.number')
    #title = music.select('td.info > a.title.ellipsis')
    #artist = music.select('td.info > a.artist.ellipsis')
    #rank = music.select_one('td.number').text.split()[0]
    #title = music.select_one('td.info > a.title.ellipsis').text.strip()
    #artist = music.select_one('td.info > a.artist.ellipsis').text
    #print(rank,title,artist)

for music in musics:
    rank = music.select_one('td.number').text.split()[0]
    title = music.select_one('td.info > a.title.ellipsis').text.strip()
    artist = music.select_one('td.info > a.artist.ellipsis').text
    print(rank,title,artist)