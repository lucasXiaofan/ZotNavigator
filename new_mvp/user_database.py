from pymongo import MongoClient

# Get database from mongodb
def get_database():
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   # The atlas url should be in .env, later add all api and url to .env
   CONNECTION_STRING = "mongodb+srv://alex01:qwer1234@uni-gpt.l7avodd.mongodb.net/"

   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
   # Create the database 
   return client['Uni-GPT']

# Retrieve User Information from database:
def retrieve_data(Collection, User_email: str):
   myquery = { "email": User_email}
   return Collection.find_one(myquery)

# Update user information
def update(collection, email, new_data):
    for key, values in new_data.items():
        if(values==""):
            continue
        collection.update_one({"email":email}, {"$set": {key:values}})   