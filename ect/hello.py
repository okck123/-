import requests
from bs4 import BeautifulSoup

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303',headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(data.text, 'html.parser')

trs = soup.select('#old_content > table > tbody > tr')

# print(trs)

# 출력 방식 순위(alt) 이름(title) 평점(point)

for tr in trs:
    title = tr.select_one('td.title > div > a')
    rank = tr.select_one('td:nth-child(1) > img')#['alt']여기에 바로 붙여도 똑같이 나옴
    # td:nth-child(1) 와 td.ac가 같은 값이 나오는 이유 => copy copyselector 했을때 #old_content > table > tbody > tr:nth-child(2) > td:nth-child(1) > img 값이나옴
    # 따라서 td:nth-child(1) > img 로도 검색이 가능하고 td.ac는 html에서 내가 td의 클래스 명이 ac 여서 써본건데 됨
    point = tr.select_one('td.point')
    if title is not None:
        title = title.text
        rank = rank['alt']
        point = point.text

        print(rank,title,point)

#from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
#client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
#db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

#db.users.delete_one({'name':'bobby'})


# import requests
# from bs4 import BeautifulSoup

# from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
# client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
# db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.


# # URL을 읽어서 HTML를 받아오고,
# headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303',headers=headers)

# # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup = BeautifulSoup(data.text, 'html.parser')

# # select를 이용해서, tr들을 불러오기
# movies = soup.select('#old_content > table > tbody > tr')

# # movies (tr들) 의 반복문을 돌리기
# for movie in movies:
#     # movie 안에 a 가 있으면,
#     a_tag = movie.select_one('td.title > div > a')
#     if a_tag is not None:
#         rank = movie.select_one('td:nth-child(1) > img')['alt'] # img 태그의 alt 속성값을 가져오기
#         title = a_tag.text                                      # a 태그 사이의 텍스트를 가져오기
#         star = movie.select_one('td.point').text                # td 태그 사이의 텍스트를 가져오기
        
#         doc ={
#             'title':title,
#             'rank':rank,
#             'star':star
#         }
#         db.movies.insert_one(doc)
