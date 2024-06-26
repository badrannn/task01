from typing import List, Optional

from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from pymongo.results import InsertOneResult
from pymongo.server_api import ServerApi

uri = "mongodb+srv://boudii2000:hDSCUD16IfPqiWaH@task01.lp8a80p.mongodb.net/?retryWrites=true&w=majority&appName=Task01"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client["tutor_database"]

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


class TutorService:

    def __init__(self):
        self.collection: Collection = db["calendar"]

    def insert_slots(self, availability_list: List[dict]):
        try:
            # Validate the structure of each document in availability_list
            # print(availability_list)
            for doc in availability_list:
                print(doc)
                if not isinstance(doc, dict):
                    raise TypeError(f"Document must be a dictionary: {doc}")
                if "day" not in doc or "available_times" not in doc:
                    raise ValueError(
                        f"Document must contain 'day' and 'available_times' keys: {doc}"
                    )

            result = self.collection.insert_many(availability_list)
            print(f"Inserted {len(result.inserted_ids)} documents")
        except Exception as e:
            print(f"Failed to insert documents: {e}")
