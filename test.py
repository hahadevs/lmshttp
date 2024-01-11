from pymongo import MongoClient


if __name__ == "__main__":
    url = "mongodb+srv://amritsingh:pHoRN47iFJs9QtkF@cluster0.pm1f2iu.mongodb.net/"
    db = MongoClient(url)
    database = db['LMS']
    collection = database['users_collection']
    for key in collection.find():
        print(key)
