import textdistance
from datetime import datetime
from pymongo import MongoClient
import config
import re
from unidecode import unidecode

from app import utility, history_repository

client = MongoClient("localhost", 27017)
db = client.market_database
list_of_matches = []


def start(db_name):
    post_process_join_duplicates(db_name)

def delete_old_ones(cursor, obj_list_retrieved):
    for i in obj_list_retrieved:
        x = cursor.delete_one(i["_id"])
        print(x)


def create_new_register(cursor, obj_list_retrieved):
    obj_to_save = obj_list_retrieved[0]
    obj_to_save["_id"] = None
    obj_to_save["price_history"] = []
    obj_to_save["dates_processed"] = []
    obj_to_save_list = []
    obj_to_delete = ""

    for i in obj_list_retrieved:
        obj_to_delete = ""
        for j in i["price_history"]:
            obj_to_save["price_history"].append(j)
        for k in i["dates_processed"]:
            obj_to_save["dates_processed"].append(k)

        obj_to_delete = i["name"]

    query_delete = {"name": obj_to_delete}
    d = cursor.delete_many(query_delete)
    print(d.deleted_count, " documents deleted !!")

    # delete_old_ones(cursor, obj_list_retrieved)
    del obj_to_save["_id"]
    x = cursor.insert_one(obj_to_save)


def post_process_join_duplicates(database):
    issue_list = []
    db_name = config.get_history_database_by_name(database)
    col_name = db[db_name]
    name_cursor = col_name.aggregate([
        {'$group': {'_id': '$name', 'count': {'$sum': 1}}},
        {'$match': {'count': {'$gt': 1}}}
    ])
    for document in name_cursor:
        name = document['_id']
        issue_list.append(name)

    for i in issue_list:
        obj_list_retrieved = []
        col_name2 = db[db_name]
        cursor = col_name2.find({"name": i})
        for doc in cursor:
            obj_list_retrieved.append(doc)
        create_new_register(col_name, obj_list_retrieved)
