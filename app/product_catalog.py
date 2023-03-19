import textdistance
from datetime import datetime
from pymongo import MongoClient
import config
import re
from unidecode import unidecode

client = MongoClient("localhost", 27017)
db = client.market_database

def start_config():
    create_main_database()

def create_main_database():
    list_to_save = []
    col = db['history_fort']
    data = col.find()

    for prod in data:
        list_to_save.append(create_and_save_product(prod["name"]))

    collection_to_save = db['product_catalog']
    x = collection_to_save.insert_many(list_to_save)


def create_and_save_product(product_name):

    return {
        "name": product_name,
        "tags": "",
        "creation_date": datetime.now()
    }