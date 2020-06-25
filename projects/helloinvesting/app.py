from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import gmtime, strftime

from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

import time


def maxnum(a,b):
    if(a>b):
        return a
    else:
        return b

def todayATRcalc(yesterdayATR,todayTR):
    return(yesterdayATR*16 + todayTR*2)/18

def todayunitcalc(investment,todayATR):
    return(investment*0.01)/todayATR

# HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/view',methods=['GET'])
def viewdata():
    datas = list(db.helloinvestment.find({},{'_id':0}))
    #현재가격을 가지고있는 리스트를 보내주자 어차피 순번은 같다.
    #datas의 name에 있는 코드를 가져와서 현재가격만 크롤링 하여 리스트에 저장후 해당 리스트를 클라이언트에 반환
    #최상단 종가가 현재가격 (계속 변동됨 주식시장 개장때는)
    nowprices = []
    for i in range(0,len(datas)):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

        driver = webdriver.Chrome('chromedriver',options=options)
        namecode = datas[i]['name']
        index = namecode.find('/') + 1
        namecode = namecode[index:]
        url = 'https://m.stock.naver.com/item/main.nhn#/stocks/' + namecode + '/price'
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        finddata = soup.find("tr",{"data-index":0}).text.split()
        nowprices.append(int(finddata[1].replace(",","")))
        driver.quit()
    return jsonify({'result': 'success','datas':datas,'nowprices':nowprices})

@app.route('/search', methods=['POST'])
def unitcalc():
    ### option 적용 ###
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    driver = webdriver.Chrome('chromedriver',options=options)
    ##################
    	# 1. 클라이언트로부터 종목코드,투자금 받기
		# 2. url페이지 크롤링후 1유닛 계산
		# 3. 클라이언트에게 1유닛 반환
    namecode_receive = request.form['namecode_give']
    investment_receive =int(request.form['investment_give'])

    url = 'https://m.stock.naver.com/item/main.nhn#/stocks/' + namecode_receive + '/price'
    # 네이버 주식페이지 url을 입력합니다.

    # 크롬을 통해 네이버 주식페이지에 접속합니다.
    driver.get(url)

    # 정보를 받아오기까지 2초를 잠시 기다립니다.
    time.sleep(2)

    # 크롬에서 HTML 정보를 가져오고 BeautifulSoup을 통해 검색하기 쉽도록 가공합니다.
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 종목이름 가져오기
    findcodename = soup.select_one('meta[property="og:title"]')['content']
    findcodename = findcodename.split()[0]
    #삼성전자 - 네이버 증권/005930 공백기준으로 문자열 분리후 index : 0 값이 종목이름값


    #20일치만 가능하니 ATR 기준을 18로 놓고 한다.
    #20일치 ATR은 20일 동안의 TR의 평균값이다 따라서 제일 최근날짜를 제외한 18일 평균으로 계산한다.
    #20일치의 날짜 종가 고가 저가를 뽑아왔다.

    date_list =[]
    ncv_list = []
    hv_list = []
    lv_list = []
    trA_list = []
    trB_list = []
    trC_list = []
    #제일 큰 tr값이 들어감
    tr_list = [] 
    # trA = todayhv-yesterdayncv 
    # trB = yesterdayncv - todaylv 
    # trC = todayhv - todaylv
    # today = i 가정시 
    # trA = hv_list[i] - ncv_list[i-1]
    # trB = ncv_list[i-1] - lv_list[i]
    # trC = hv_list[i] - lv_list[i]
    for i in range(0,19):
        finddata = soup.find("tr",{"data-index":i}).text.split()
        date_list.append(finddata[0])
        ncv_list.append(int(finddata[1].replace(",","")))
        hv_list.append(int(finddata[5].replace(",","")))
        lv_list.append(int(finddata[6].replace(",","")))
    date_list.reverse()
    ncv_list.reverse()
    hv_list.reverse()
    lv_list.reverse()
    #TR 계산식
    for i in range(1,19):
        trA_list.append(hv_list[i] - ncv_list[i-1])
        trB_list.append(hv_list[i-1] - ncv_list[i])
        trC_list.append(hv_list[i] - ncv_list[i])
    #콤마를 최대 2개는 지워줘야한다 1,000,000 백만단위 이상 주식이 한국엔 없기때문
    for i in range(0,18):
        tr = maxnum(trA_list[i],trB_list[i])
        tr_list.append(maxnum(tr,trC_list[i]))
    #전날 ATR
    ATRSum = 0
    for i in range(0,16):
        ATRSum = ATRSum + tr_list[i]
    yesterdayATR = ATRSum/16
    #당일 ATR
    todayATR = todayATRcalc(yesterdayATR,tr_list[17])
    
    unit = todayunitcalc(investment_receive,todayATR)
    unitshare = round(unit)
    unitwon = unitshare*ncv_list[18]
    
    print(unitshare,unitwon)
    
    driver.quit()

    resultcodename = findcodename +"/"+ namecode_receive
    resultunit = str(unitwon) + "/" + str(unitshare)

    doc = {
        'date' : datetime.today().strftime("%Y.%m.%d %H:%M:%S"),
        'name' : resultcodename,
        'investment' : investment_receive,
        'unit' : resultunit,
        'searchprice' : ncv_list[18]
    }

    db.helloinvestment.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '계산 완료!','unitshare':unitshare,'unitwon':unitwon})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)
















