import textdistance
from datetime import datetime
from pymongo import MongoClient
import config
import re
from unidecode import unidecode

from app import utility, history_repository, service_remove_duplicates

client = MongoClient("localhost", 27017)
db = client.market_database
list_of_matches = []


def start_alternate():
    histories_databases = config.get_history_databases()
0
    for db in histories_databases:
        collection_name = histories_databases["collection"]
        col = db[collection_name]
        data = col.find()

def start():
    price_db = config.get_price_databases()

    for database in price_db:
        collection_name = database["collection"]
        collection = db[collection_name]
        all_price_documents_for_one_pos = collection.find()
        for price_document_for_a_day in all_price_documents_for_one_pos:
            print("Processando: ", database["name"], "... ")
            update_history(database["name"], price_document_for_a_day)
        ### Theres an issue that must be solved
        ### Some products get to be duplicated, until the reason is figured out
        ### This service must be executed
        service_remove_duplicates.start(database["name"])


def update_history(pdv_name, data):
    for category in data["categories_list"]:
        process_category(pdv_name, category, data["date_time"])


def lists_are_up_to_date(price_extraction_date, product_list):
    for i in product_list:
        if price_extraction_date in i["dates_processed"]:
            return True
        else:
            return False


def process_category(pdv_name, category, price_extraction_date):
    category_name = category["category_name"]

    for subcategory in category["subcategory_list"]:
        history_collection_name = config.get_history_database_by_name(pdv_name)
        product_list = history_repository.get_products_by_subcategory(subcategory["subcategory_name"].lower(), history_collection_name)

        print("Processando: ", category_name, " subcategoria: ", subcategory["subcategory_name"].lower(), "em ", price_extraction_date)

        if lists_are_up_to_date(price_extraction_date, product_list):
            break
        else:
            process_products_lists(pdv_name, product_list, subcategory["product_list"], category_name,
                                   subcategory["subcategory_name"], price_extraction_date)



def process_products_lists(pdv_name, list_old, list_new, category_name, subcategory_name, product_extraction_date):
    list_of_matches = []
    for item in list_new:
        history_product = {}
        if len(item) == 6:
            if list_old == []:
                list_of_dates_processed = [product_extraction_date]
                product_to_save = process_product(pdv_name, item, category_name, subcategory_name,
                                                  product_extraction_date, list_of_dates_processed)
                history_repository.update_product_history(pdv_name, product_to_save["name"],
                                                          product_to_save["price_history"][0]["price"],
                                                          product_to_save["price_history"][0]["date"],
                                                          product_to_save)
            else:
                history_product = get_history_product(item, list_old, pdv_name)
                if history_product == '':
                    list_of_dates_processed = [product_extraction_date]
                    product_to_save = process_product(pdv_name, item, category_name, subcategory_name,
                                                      product_extraction_date, list_of_dates_processed)
                    history_repository.save_product(pdv_name, product_to_save)
                    pass
                else:
                    if utility.is_date_prod_extracted_biggest_than_last_prod_in_history(history_product,
                                                                                product_extraction_date):
                        update_history_product(pdv_name, history_product, item, product_extraction_date)
                    else:
                        pass
        else:
            # ignorando itens que possuem tamanho incompleto, dados sujos, etc.,
            pass


def add_item_to_list_of_found_matches(item_name):
    list_of_matches.append(item_name)


def is_item_in_list_found_matches(item_name):
    is_item_found = False

    for i in list_of_matches:
        if i == item_name:
            is_item_found = True

    return is_item_found


def get_history_product(item, list_old, pdv_name):
    has_found_equal = False
    history_product_found = {}

    item_name = ''
    for history_product in list_old:
        has_found_equal = False
        ##testing...
        item_name = unidecode(item["name"].lower())
        if item_name == history_product["name"]:
            has_found_equal = True
            add_item_to_list_of_found_matches(item_name)
            history_product_found = history_product
            break

    if has_found_equal:
        return history_product_found

    if not has_found_equal:
        if not is_item_in_list_found_matches(item_name):
            item_name = unidecode(item["name"].lower())
            item_name = utility.transform_name(item_name)
            collection_name = config.get_history_database_by_name(pdv_name)
            col = db[collection_name]
            myquery = {"name": item_name}
            data = col.find_one(myquery)
            if data is not None:
                if data["name"] == item_name:
                    return data

    return ''


# def process_subcategory(name, subcategory, category_name):
#     subcategory_name = subcategory["subcategory_name"]
#     for product in subcategory["product_list"]:
#         process_product(name, product, category_name, subcategory_name)
def update_history_product(pdv_name, history_product, item, date):
    double_price = utility.get_double_price(item["price"])
    history_product["price_history"].append({
        "date": date,
        "price": double_price
    })
    history_product["dates_processed"].append(date)
    collection_name = config.get_history_database_by_name(pdv_name)
    collection = db[collection_name]
    cursor = collection.replace_one({"_id": history_product["_id"]}, history_product)


def process_product(pdv_name, product, category, subcategory, date, dates_processed):
    if len(product) < 6:
        return ''

    product_name = unidecode(product["name"].lower())
    category_name = unidecode(category.lower())
    subcategory_name = unidecode(subcategory.lower())
    double_price = utility.get_double_price(product["price"])

    product_name = utility.transform_name(product_name)

    product = {
        "name": product_name,
        "update_at": datetime.now(),
        "category": category_name,
        "subcategory": subcategory_name,
        "thumbnail": product["thumbnail"],
        "link": product["link"],
        "price_history": [{
            "price": double_price,
            "date": date
        }],
        "dates_processed": dates_processed
    }

    return product

