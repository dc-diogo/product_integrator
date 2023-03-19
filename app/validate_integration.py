import random
from pymongo import MongoClient
import config
import csv


from app import integrator

client = MongoClient("localhost", 27017)
db = client.market_database
header = ["pdv_name", "product_catalog_name", "candidates", "name_history", "score_damerau_levenshtein", "score_jaro_winkler", "weight"]
all_rows = []

def get_random(data):

    prod_list = []

    for prod in data:
        prod_list.append(prod)

    cont = 550
    i = 0
    random_prod_list = []

    while i < cont:
        random_prod_list.append(random.choice(prod_list))
        i = i + 1

    return random_prod_list

def start():
    print("FUCKING")
    sample_test_creation()
    col = db['product_catalog']
    data = col.find()
    product_list_to_index = get_random(data)

    history = config.get_history_databases()

    for database in history:
        collection_name = database["collection"]
        hist = db[collection_name]
        history_object_doc_list = hist.find()
        test_products = []

        for history_object_list in history_object_doc_list:
            test_products.append(history_object_list)

        integrator.start_comparasion(test_products, product_list_to_index, database["name"])

def sample_test_creation():
    col = db['index_product_teste']
    data = col.find()
    product_list_to_index = get_random(data)
    rows_saved = []

    for doc in product_list_to_index:
        if len(doc["pdvs"]) == 3:
            best_candidates = get_best_candidates(doc)
            rows_saved.append(best_candidates)

    with open('testes.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write multiple rows
        for i in rows_saved:
            writer.writerows(i)

def get_best_candidates(doc):
    text_line = []
    row_line = []
    selected_candidate = None

    for pdv in doc["pdvs"]:
        text_line.clear()
        row_line.clear()
        for d in pdv["candidates"]:
            text_line = []
            text_line.append(pdv["pdv_name"])
            text_line.append(doc["product_catalog_name"])
            text_line.append(d["name_history"])
            text_line.append(d["score_damerau_levenshtein"])
            text_line.append(d["score_jaro_winkler"])
            text_line.append(d["weight"])
            row_line.append(text_line)
            selected_candidate = get_best_candidate(row_line)

        all_rows.append(selected_candidate)

    return all_rows

def get_best_candidate(rows):
    rows.sort(key=lambda x: float(x[4]))
    return rows[len(rows)-1]



def sort_func(x):
    return -x['weight']


