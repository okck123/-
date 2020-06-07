from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

import js2py

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')


@app.route('/search', methods=['get'])
def search():
		# 1. 클라이언트로부터 종목이름 받기
		# 2. url페이지 크롤링
		# 3. 클라이언트에게 종목코드 반환
    url_receive = 'https://datamall.koscom.co.kr/kor/datamall/stock/popSearchStockCode.do#'
    name_receive = '삼성전자'
    
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    #document.getElementById('stdCodeName').value = '종목이름'
    #document.getElementById("searchBtn").click();

    codetext = """
    document.getElementById('stdCodeName').value = ${name_recive}
    """
    codebtn = """
    document.getElementById("searchBtn").click();
    """
    
    codename = soup.select_one('lpop_content > div.default_view > div > div.itemSrc_l > table > tbody > tr:nth-child(2) > td > div > stockCodeList > option:nth-child(1)')

    print(codename)
    return jsonify({'result': 'success', 'codename':codename})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)


   
   #lpop_content > div.default_view > div > div.itemSrc_l > table > tbody > tr:nth-child(2) > td > div
   #stdCodeName 여기에 종목이름 넣기
    ##stockCodeList > option:nth-child(1) 이값 가져오기