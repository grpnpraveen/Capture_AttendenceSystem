from pymongo import MongoClient
import pymongo
def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    return client['BML']

dbname = get_database()

todo=dbname["PA_SUB_DDMNYY_HHMM_UNIQCODE"]
for i in range(9):
    item_1 = {
    "_id":"REGNO"+str(i),
    "present":"1/0",
    }
    todo.insert_one(item_1)
# id="REGNO0"
# item_details=todo.find()
# print(todo)
# for item in item_details:
#     # This does not give a very readable output
#     if item["_id"]==id:
#         print(item)