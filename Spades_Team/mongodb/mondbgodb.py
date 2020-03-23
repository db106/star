# import
import os
import json
# need pip
from pymongo import MongoClient
#from bson.objectid import ObjectId #這東西再透過ObjectID去尋找的時候會用到


def connect_mongodb(db_name,collection_name):
	global collection
	# connection
	conn = MongoClient("mongodb://127.0.0.1") # 如果你只想連本機端的server你可以忽略，遠端的url填入: mongodb://<user_name>:<user_password>@ds<xxxxxx>.mlab.com:<xxxxx>/<database_name>，請務必既的把腳括號的內容代換成自己的資料。
	db = conn[db_name]
	collection = db[collection_name]

	# collection.remove({})

def mongodb_insert(json):

	collection.insert(json)

def mongodb_find():
	for doc in collection.find():
		print(doc)

def main():
	i = 0
	dir_path = 'E:/資策會-DB106/專題/Pixnet/All'
	for each_dir in os.listdir(dir_path):
		if '景點' in each_dir:
			connect_mongodb("spades", "play")
		elif '美食' in each_dir:
			connect_mongodb("spades", "food")
		# print(each_dir)
		dir_path_play_food = dir_path + "/" + each_dir
		for each_txt in os.listdir(dir_path_play_food):
			if '_record_article.txt' != each_txt:
				# print(each_txt)
				with open(dir_path_play_food + '/' + each_txt, 'r', encoding='utf8') as f:
					for txt in f.read().split('\n-----'):
						if txt != '\n':
							txt = json.loads(txt)
							print(txt)
							mongodb_insert(txt)
							i += 1

	connect_mongodb("spades", "play")
	print(collection,'count:',collection.count())
	collection.remove({})
	connect_mongodb("spades", "food")
	print(collection, 'count:', collection.count())
	collection.remove({})
	print(i)
# # test if connection success
# collection.stats  # 如果沒有error，你就連線成功了。
# print(collection.stats)


if __name__ == '__main__':

    main()
    print('Complete!!!!!!!!!!')
