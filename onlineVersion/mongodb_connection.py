from pymongo import MongoClient
from typing import Any, Dict, Optional
from pymongo import MongoClient
from urllib.parse import quote_plus

class MongoDBManager:
    def __init__(self):
        """Initialize MongoDB connection"""
        username = quote_plus('lucaswe957')
        password = quote_plus('e3b1Df3nQ3QkzEo5')
        cluster = 'cluster0.rg0ja.mongodb.net'
        uri = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=Cluster0"

        self.client = MongoClient(uri)



        self.current_db = None
        self.current_collection = None
        
    def use_database(self, database_name: str) -> None:
        """Select a database to use, creates it if it doesn't exist"""
        self.current_db = self.client[database_name]
        # MongoDB creates the database when we first store data
        
    def use_collection(self, collection_name: str) -> None:
        """Select a collection to use, creates it if it doesn't exist"""
        if self.current_db is None:
            raise ValueError("No database selected. Call use_database first.")
        self.current_collection = self.current_db[collection_name]
        # MongoDB creates the collection when we first store data
        
    def insert_document(self, document: Dict[str, Any], natural_name: str) -> str:
        """
        Insert a document with a natural language name
        Returns: The natural language name used for the document
        """
        if self.current_collection is None:
            raise ValueError("No collection selected. Call use_collection first.")
            
        # Convert natural name to underscore format and ensure uniqueness
        formatted_name = natural_name.lower().replace(' ', '_')
        
        # Add the natural name to the document
        document['_natural_name'] = formatted_name
        
        # Check if a document with this name already exists
        existing = self.current_collection.find_one({'_natural_name': formatted_name})
        if existing:
            raise ValueError(f"Document with name '{formatted_name}' already exists")
            
        # Insert the document
        self.current_collection.insert_one(document)
        return formatted_name
        
    def get_document_by_name(self, natural_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve a document using its natural language name"""
        if self.current_collection is None:
            raise ValueError("No collection selected. Call use_collection first.")
            
        formatted_name = natural_name.lower().replace(' ', '_')
        document = self.current_collection.find_one({'_natural_name': formatted_name})
        
        if document:
            return document
        return None
        
    def list_document_names(self) -> list:
        """List all natural names of documents in the current collection"""
        if self.current_collection is None:
            raise ValueError("No collection selected. Call use_collection first.")
            
        return [doc['_natural_name'] for doc in self.current_collection.find({}, {'_natural_name': 1})]

# Example usage:
if __name__ == "__main__":
    # Initialize connection
    CONNECTION_STRING = "mongodb://w95731D3Q3QkzEo5@0.g0jmg/?yW=&=mjiy&p=Cr0"
    db = MongoDBManager()
    
    # Use a database and collection
    db.use_database("example_db")
    db.use_collection("example_collection")
    
    # Insert a document with a natural name
    doc = {
        "title": "Example Document",
        "content": "This is an example"
    }
    name = db.insert_document(doc, "My First Document")
    
    # Retrieve the document
    retrieved_doc = db.get_document_by_name("My First Document")
    if retrieved_doc:
        print(f"Found document: {retrieved_doc}")
    
    # List all document names
    names = db.list_document_names()
    print(f"All document names: {names}")
