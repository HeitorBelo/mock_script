import pymongo
from dotenv import load_dotenv
from os import getenv
from time import sleep
from itertools import chain

class SaveOnMongo:
    def __init__(self):
        load_dotenv()
        self.client = pymongo.MongoClient(getenv("MONGO_URL"))
        self.db = self.client[getenv("MONGO_DATABASE")]
        self.consumer_collection = self.db[getenv("MONGO_CONSUMERS_COLLECTION_NAME")]
        self.transactions_collection = self.db[getenv("MONGO_TRANSACTIONS_COLLECTION_NAME")]

    def save_consumers(self, consumers):
        try:
            self.consumer_collection.insert_many(consumers)
        except Exception as e:
            print(f"Erro ao salvar consumidor: {e}")

    def save_transactions(self, transactions):
        # "Flatten" a lista de listas usando itertools.chain
        flat_transactions = list(chain.from_iterable(transactions))
        try:
            # Realiza o insert_many com todos os documentos
            self.transactions_collection.insert_many(flat_transactions)
        except Exception as e:
            print(f"Erro ao salvar transactions: {e}")
