from selenium import webdriver
from bs4 import BeautifulSoup

import time

def maxnum(a,b):
    if(a>b):
        return a
    else:
        return b

def todayATRcalc(yesterdayATR,todayTR):
    return(yesterdayATR*16 + todayTR*2)/18

# 셀레니움을 실행하는데 필요한 크롬드라이버 파일을 가져옵니다.
driver = webdriver.Chrome('chromedriver')

# 네이버 주식페이지 url을 입력합니다.
url = 'https://m.stock.naver.com/item/main.nhn#/stocks/005930/price'

# 크롬을 통해 네이버 주식페이지에 접속합니다.
driver.get(url)

# 정보를 받아오기까지 2초를 잠시 기다립니다.
time.sleep(2)

# 크롬에서 HTML 정보를 가져오고 BeautifulSoup을 통해 검색하기 쉽도록 가공합니다.
soup = BeautifulSoup(driver.page_source, 'html.parser')

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
# 1유닛 주/원
unit = (1000000*0.01)/todayATR
roundunit = round(unit)

print(roundunit,ncv_list[18]*roundunit)

#이걸 DB에 저장

# 크롬을 종료합니다.
driver.quit()

# HTML을 주는 부분
@app.route('/')
def home():
   #return render_template('index.html')

@app.route('/search', methods=['get'])
def unitcalc():
		# 1. 클라이언트로부터 종목코드,투자금 받기
		# 2. url페이지 크롤링후 1유닛 계산
		# 3. 클라이언트에게 1유닛 반환
    return jsonify({'result': 'success', 'codename':codename})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)
















