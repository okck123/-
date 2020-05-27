from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/orders', methods=['POST'])
def save_order():
    ## 1. input 데이터 받고
    ## 2. mongoDB에 데이터 넣기

    UsernameText_receive = request.form['UsernameText_give']
    Count_receive = request.form['Count_give']
    AddressText_receive = request.form['AddressText_give']
    PhonenumberText_receive = request.form['PhonenumberText_give']
        
    doc = {
        'Username' : UsernameText_receive,
        'Count' : Count_receive,
        'Address' : AddressText_receive,
        'Phonenumber' : PhonenumberText_receive
    }

    db.orders.insert_one(doc)
    return jsonify({'result':'success', 'msg': '주문 완료!'})


@app.route('/orders', methods=['GET'])
def show_order():
    ## db에 저장된 값을 불러오기
    ## 따로 메세지는 필요없다.
    ## table에 양식에 맞게 넣어주기
    orders = list(db.orders.find({},{'_id':0}))
    return jsonify({'result':'success', 'orders': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)