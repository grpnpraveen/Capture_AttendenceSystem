from pymongo import MongoClient
# import pymongo
def get_database(DB):
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://admin:root@cluster0.cjpup.mongodb.net/crud_mongodb?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    return client[DB]

dbname = get_database("getdata")

todo=dbname["PA"]

id="BML_PA_WD_13112021_1500_24269"
item_details=todo.find()
# print(todo)
for item in item_details:
    # This does not give a very readable output
    if item["code"]==id:
        print(item)