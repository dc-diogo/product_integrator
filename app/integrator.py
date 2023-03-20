import textdistance
from datetime import datetime
from pymongo import MongoClient
import config
import tests
import re
from unidecode import unidecode
from difflib import SequenceMatcher

client = MongoClient("localhost", 27017)
db = client.market_database


def start():
    history = config.get_history_databases()
    for database in history:
        collection_name = database["collection"]
        col = db[collection_name]
        history_object_doc_list = col.find()
        product_catalog = tests.test_products()
        products_list_history = tests.get_docs_with_popular_products(history_object_doc_list)
        for history_object_list in products_list_history:
            start_comparasion(history_object_list, product_catalog, database["name"])


def start_comparasion(history_object_list, product_catalog, pdv_name):
    calculate_common_sequence(history_object_list, product_catalog,
                              pdv_name)


def calculate_common_sequence(history_object_list, product_catalog, pdv_name):

    for index_item in product_catalog:
        candidate_list = []
        product_index_list = []

        for product_history in history_object_list:
            possible_candidate = compara_index_com_produto(index_item, product_history)

            if possible_candidate is not None:
                candidate_list.append(possible_candidate)

            if len(candidate_list) > 0:
                collection_to_save = db['index_product_teste']

            try:
                obj_found = collection_to_save.find_one({"product_catalog_id": index_item["_id"]})
                if obj_found:
                    update_index_document(obj_found, candidate_list, pdv_name)
                else:
                    create_new_index(index_item, candidate_list,pdv_name)
            except:
                print("Connection error...")


def update_index_document(obj_found, candidate_list, pdv_name):
    pdvs = obj_found["pdvs"]
    pdv_already_inserted = False
    for pdv in pdvs:
        if pdv["pdv_name"] == pdv_name:
            pdv_already_inserted = True
    candidates = pdv["candidates"]
    for i in candidate_list:
        candidates.append(i)
    if not pdv_already_inserted:
        pdvs.append({
            "pdv_name": pdv_name,
            "candidates": candidate_list
        })
    myquery = {"_id": obj_found["_id"]}
    newvalues = {"$set": {"pdvs": pdvs}}
    collection_to_save = db['index_product_teste']
    collection_to_save.update_one(myquery, newvalues)


def create_new_index(index_item, candidate_list, pdv_name):
    index_document = create_index_document(index_item, candidate_list,
                                           pdv_name)
    collection_to_save = db['index_product_teste']
    x = collection_to_save.insert_one(index_document)


def compara_index_com_produto(indice, produto):
    resultado_comparacao_substring = textdistance.lcsstr(indice["name"],
                                                         produto["name"])
    product_result_splitted = resultado_comparacao_substring.split()
    name_indice = indice["name"]
    name_produto = produto["name"]
    split_name_indice = indice["name"]
    split_name_produto = produto["name"].split()

    if "litro" in product_result_splitted:
        product_result_splitted.remove("litro")
    if "gramas" in product_result_splitted:
        product_result_splitted.remove("gramas")

    if len(product_result_splitted) > 0:
        for i in product_result_splitted:
            if i.isnumeric():
                product_result_splitted.remove(i)

    if len(product_result_splitted) > 0:
        if get_numbers(produto["name"]) == get_numbers(indice["name"]):
            return continua(split_name_produto, indice["name"].split(), indice, produto)
        else:
            print("Unidade does not match...")
    else:
        print("Less than 1 match in substring sequence...")

    return None


def calculate_edit_distance(indice, produto):
    jaro_winkler = textdistance.jaro_winkler(indice["name"], produto["name"])
    damerau_levenshtein = textdistance.damerau_levenshtein(indice["name"], produto["name"])
    return {"damerau_levenshtein": damerau_levenshtein, "jaro_winkler": jaro_winkler}


def continua(product_splited, index_splited, indice, produto):
    matches_identical_count = 0
    identical_words_list = []
    for prod in product_splited:

        # Match em palavras com tres ou menos caracteres são descosiderados
        if len(prod) > 3:
            for i in index_splited:
                if prod == i:
                    matches_identical_count = matches_identical_count + 1
        identical_words_list.append(prod)
        if matches_identical_count != 0:
            edit_distance_result = calculate_edit_distance(indice, produto)
            return create_candidate(produto, matches_identical_count, identical_words_list, edit_distance_result)
        return None


def create_index_document(indice, candidate_list, pdv_name):
    return {
        "product_catalog_id": indice["_id"],
        "product_catalog_name": indice["name"],
        "pdvs": [{"pdv_name": pdv_name, "candidates": candidate_list}]
    }


def create_candidate(produto, matches_identical_count, identical_words_list, edit_distance_result):
    return {
        "id": produto["_id"],
        "name_history": produto["name"],
        "score_damerau_levenshtein":
            edit_distance_result["damerau_levenshtein"],
        "score_jaro_winkler": edit_distance_result["jaro_winkler"],
        "weight": matches_identical_count,
        "identical_words": identical_words_list
    }


def get_numbers(new_string):
    str_nmb = ""
    for m in new_string:
        if m.isdigit():
            str_nmb = str_nmb + m
    return str_nmb


def compare(i, comparable_item, service_name):
    result = None
    try:
        if service_name == 'HAMMING':
            result = textdistance.hamming(i, comparable_item)
        if service_name == 'LEVENSHTEIN':
            result = textdistance.levenshtein(i, comparable_item)
        if service_name == 'JARO_WINKLER':
            result = textdistance.jaro_winkler(i, comparable_item)
        if service_name == 'jaccard':
            result = textdistance.jaccard(i, comparable_item)
        if service_name == 'lcsstr':
            result = textdistance.lcsstr(i, comparable_item)
        if service_name == 'lcsseq':
            result = textdistance.lcsseq(i, comparable_item)
        if service_name == 'DAMERAU_LEVENSHTEIN':
            result = textdistance.damerau_levenshtein(i, comparable_item)
    except:
        print(i)
        print("not found ----------------------------------------------------")
        print(f"{service_name};{i};{comparable_item};{result}")
