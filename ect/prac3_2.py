from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

#내가 작성한 코드
Matrixstar = list(db.movies.find({'title' : '매트릭스'}))
Matrixstar2 = db.movies.find_one({'title':'매트릭스'})

print(Matrixstar[0]['star'])
print(Matrixstar2['star'])

#튜터님이 작성한 코드
target_movie = db.movies.find_one({'title':'매트릭스'})
print(target_movie['star'])

#내가 작성한 코드
all_movies = list(db.movies.find())

for movie in all_movies:
    if movie['star'] == Matrixstar2['star']:
        print(movie['title'])

#튜터님이 작성한 코드
target_star = target_movie['star']

movies = list(db.movies.find({'star':target_star},{'_id':False}))

for movie in movies:
    print(movie['title'])

#내가 작성한 코드 '매트릭스' 의 평점은 9.39이다 
#db.movies.update_many({'star' : Matrixstar2['star']},{'$set' : {'star': 0}})

#튜터님이 작성한 코드
db.movies.update_many({'star' : target_star},{'$set':{'star':0}})