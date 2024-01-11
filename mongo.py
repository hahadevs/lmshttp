from pymongo import MongoClient

class MongoDatabase:
    def __init__(self):
        self.conn = False
    
    def connect(self):
        with open('mongo.conf','r') as conf_file:
            conn_url = conf_file.read()
        self.conn = MongoClient(conn_url)
        self.lms_database = self.conn['LMS']
        self.users_collection = self.lms_database['users_collection']
    def create_user(self,user_dict):
        new_user = {
            user_dict['email']:
            {
                'firstname':user_dict['firstname'],
                'lastname':user_dict['lastname'],
                'password':user_dict['password'],
                'current_borrow':[]
            }
        }
        self.users_collection.insert_one(new_user,bypass_document_validation=False,comment=None,session=None)
        print("New user added : ",user_dict['email'])
    def get_users_collection(self):
        collection = self.users_collection.find()
        return collection
    def is_user_exists(self,email):

        return False
    def __del__(self):
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    obj = MongoDatabase()
    obj.connect()
    print(obj.get_users_collection())
    # obj.create_user({
    #     "email":"new@gmail.com",
    #     "firstname":"fname",
    #     "lastname":"lastname",
    #     "password":"123"
    # })