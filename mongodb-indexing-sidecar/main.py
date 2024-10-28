import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')


def create_indexes():
    """
    Connects to the MongoDB instance and creates indexes on the 'transactions' collection.

    Indexes created:
    - Single-field index on 'transaction_hash'
    - Single-field index on 'timestamp'
    """
    print("Adding indexes...")
    client = MongoClient(MONGODB_URL)
    db = client['transactions']
    collection = db['transactions']

    collection.create_index([('transaction_hash', 1)])
    collection.create_index([('timestamp', 1)])
    print("Indexes added. Exiting job.")


if __name__ == '__main__':
    create_indexes()
