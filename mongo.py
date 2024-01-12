from pymongo import MongoClient
from datetime import datetime
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
    def create_transaction(self,username,bookid,action) -> str:
        details = {
            'username':username,
            'bookid':bookid,
            'date':str(datetime.now().date()),
            'action':action
        }
        transaction_obj = self.records_collection.insert_one(details)
        return transaction_obj.inserted_id
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
    def __del__(self):
        if self.conn:
            self.conn.close()


# if __name__ == "__main__":
    # obj = MongoDatabase()
    # obj.connect()
    # print(obj.get_users_collection_list())