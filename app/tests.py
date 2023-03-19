import textdistance
from datetime import datetime
from pymongo import MongoClient
import config
import re
from unidecode import unidecode

client = MongoClient("localhost", 27017)
db = client.market_database
list_of_matches = []

serch_index_collection = db["product_catalog"]
serch_index_doc_list = serch_index_collection.find()


def get_tests_lists():
    pipoca_list = []
    leite_list = []
    veja_list = []
    detergente_list = []
    arroz_list = []

    for doc in serch_index_doc_list:
        if "leite" in doc["name"]:
            leite_list.append(doc)
        if "pipoca" in doc["name"]:
            pipoca_list.append(doc)
        if "veja" in doc["name"]:
            veja_list.append(doc)
        if "detergente" in doc["name"]:
            detergente_list.append(doc)
        if "arroz" in doc["name"]:
            arroz_list.append(doc)

    return [pipoca_list, leite_list, veja_list, detergente_list, arroz_list]


def get_docs_with_popular_products(history_object_doc):
    leite_list_history = []
    amaciante_list_history = []
    cafe_list_history = []
    maionese_list_history = []

    for i in history_object_doc:
        if "leite" in i["name"]:
            leite_list_history.append(i)
        if "amaciante" in i["name"]:
            amaciante_list_history.append(i)
        if "cafe" in i["name"]:
            cafe_list_history.append(i)
        if "maionese" in i["name"]:
            maionese_list_history.append(i)

    return [leite_list_history, amaciante_list_history, cafe_list_history, maionese_list_history]


def test_products():
    products = [
        {
            "id": "62b1231e72ab3382a5958b7b",
            "name": "amaciante de roupas concentrado downy naturals coco e menta 450ml"
        },
        {
            "id": '62b1231e72ab3382a5958383',
            "name": 'leite tirol integral 1 litro'
        },
        {
            "id": '62b1231e72ab3382a595895e',
            "name": 'maionese hemmer tradicional 930g'
        },
        {
            "id": '62b1231e72ab3382a5958b52',
            "name": 'amaciante para roupas concentrado downy brisa de verao 1,5 litro'
        },
        {
            "id": '62b1231e72ab3382a5958386',
            "name": 'cafe melitta tradicional vacuo 500g'
        },

    ]

    return products