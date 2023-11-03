from pymongo import MongoClient
def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   # The atlas url should be in .env, later add all api and url to .env
   CONNECTION_STRING = "mongodb+srv://alex01:qwer1234@uni-gpt.l7avodd.mongodb.net/"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)

   # Create the database for our example 
   return client['Uni-GPT']

