from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
class MongoDatabase:
    def __init__(self):
        self.conn = False 
    def connect(self):
        with open('mongo.conf','r') as conf_file:
            conn_url = conf_file.read()
        self.conn = MongoClient(conn_url)
        self.lms_database = self.conn['LMS']
        self.__admin_auth = self.lms_database['admin_auth']
        self.users_collection = self.lms_database['users_collection']
        self.books_collection = self.lms_database['books_collection']
        self.records_collection = self.lms_database['records_collection']
    def create_user(self,user_dict):
        new_user = {
            'email':user_dict['email'],
            'firstname':user_dict['firstname'],
            'lastname':user_dict['lastname'],
            'password':user_dict['password'],
            'current_borrow':[]
        }
        self.users_collection.insert_one(new_user,bypass_document_validation=False,comment=None,session=None)
    def create_transaction(self,username:str,bookid:str,action:str) -> str:
        """Updating Books Collection to decrement book by 1"""
        if action == "borrow": inc = -1
        elif action == "return" : inc = +1
        else:raise Exception("Invalid action value for transaction ")
        self.books_collection.update_one({"_id":ObjectId(bookid)},{"$inc":{"quantity":inc}})
        """Updating Users bag with new book"""
        mybag = self.users_collection.find_one({"email":username})['mybag']
        if action == 'borrow':
            mybag.append(bookid)
        elif action == 'return':
            mybag.remove(bookid)

        """Creating a transaction"""
        details = {
            'username':username,
            'bookid':bookid,
            'date':str(datetime.now().date()),
            'action':action
        }
        self.users_collection.update_one({"email":username},{"$set":{"mybag":mybag}})
        transaction_obj = self.records_collection.insert_one(details)
        return transaction_obj.inserted_id
    def add_book(self,details_dict:dict):
        book_details = {
            'title':details_dict['title'],
            'author':details_dict['author'],
            'isdn':details_dict['isdn'],
            'quantity':int(details_dict['quantity']),
            'genre':[],
            'status':int(details_dict['status'])
        }
        self.books_collection.insert_one(book_details)
    def get_mybag(self,user_email:str)->list:
        mybag = self.users_collection.find_one({"email":user_email})['mybag']
        list_mybag_dict = []
        for book_id in mybag:
            list_mybag_dict.append(self.books_collection.find_one({"_id":ObjectId(book_id)}))
        return list_mybag_dict
    def get_book_dict(self,book_id:str):
        return self.books_collection.find_one({"_id":ObjectId(book_id)})
    def get_list_transactions(self,filter:dict=None) -> list:
        if filter:
            return [record for record in self.records_collection.find(filter)]
        return [record for record in self.records_collection.find()]
    def get_list_books(self,filter:dict=None) -> list:
        if filter:
            return [book for book in self.books_collection.find(filter)]
        return [book for book in self.books_collection.find()]
    def get_list_users(self,filter:dict=None) -> list:
        if filter:
            return [user for user in self.users_collection.find(filter)]
        return [document for document in self.users_collection.find()]
    def is_user_exists(self,credentials) -> dict:
        found_list = list(self.users_collection.find({"email":credentials['username'],'password':credentials['password']}))
        if len(found_list) == 1:
            return found_list[0]
    def is_libadmin(self,credentials) -> dict:
        found_list = list(self.__admin_auth.find({"email":credentials['username'],'password':credentials['password']}))
        print(found_list)
        if len(found_list) == 1 :
            return found_list[0]
    def delete_book(self,req_dict):
        _id = ObjectId(req_dict["_id"])
        # self.books_collection.delete_one({"_id":_id})
        for book in self.books_collection.find({"_id":_id}):
            print("book found and testing purpose delete : ",book["_id"])

    def __del__(self):
        if self.conn:
            self.conn.close()


# if __name__ == "__main__":
    # obj = MongoDatabase()
    # obj.connect()
    # print(obj.get_users_collection_list())