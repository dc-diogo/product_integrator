from datetime import datetime

from pymongo import MongoClient
import config

client = MongoClient("localhost", 27017)
db = client.market_database

def save_product(pos_name, product):
    collection_name = config.get_history_database_by_name(pos_name)
    collection = db[collection_name]

    try:
        x = collection.insert_one(product)
    except:
        print("error saving object")

def update_product_history(pos_name, product_name, product_price, product_extraction_date, product):
    collection_name = config.get_history_database_by_name(pos_name)
    collection = db[collection_name]

    doc = collection.find_one({'name': product_name})
    if doc:
        # Update the document fields
        now = datetime.now()
        doc['update_at'] = now
        doc['price_history'].append({
            'price': product_price,
            'date': product_extraction_date
        })
        doc['dates_processed'].append(product_extraction_date)

        # Update the document in the collection

    try:
        collection.replace_one({'_id': doc['_id']}, doc)
    except:
        print("error updating object")
        save_product(pos_name, product)

def get_products_by_subcategory(subcategory, collection_name):
    collection = db[collection_name]
    cursor = collection.find({"subcategory": subcategory})
    lista = []
    for record in cursor:
        lista.append(record)

    return lista