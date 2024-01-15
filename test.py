from pymongo import MongoClient
from bson import ObjectId

if __name__ == "__main__":
    url = "mongodb+srv://amritsingh:pHoRN47iFJs9QtkF@cluster0.pm1f2iu.mongodb.net/"
    db = MongoClient(url)
    database = db['LMS']
    books = database['users_collection']
    books.update_one({"email":"unique@gmail.com"},{"$set":{"mybag":["book1"]}})
    print(books.find_one({"email":"unique@gmail.com"})['mybag'])
    # for book in books.find():
        # print(book['status'])
        # print(type(book['status']))



