from pymongo import MongoClient
import schedule
import time
import gs_fort
import gs_bistek
import gs_hippo
import gs_imperatriz
import numpy as np


def job():
    print("I'm working...")


def agendamento():
    schedule.every().day.at("23:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


def production():
    client = MongoClient("localhost", 27017)

    db = client.market_database
    db.list_collection_names()

    FORT_DB = db.fort
    gs_fort.start(FORT_DB)

    BISTEK_DB = db.bistek
    gs_bistek.bistek_start(BISTEK_DB)

    IMPERATRIZ_DB = db.imperatriz
    gs_imperatriz.start(IMPERATRIZ_DB)

    HIPPO_DB = db.hippo
    gs_hippo.start(HIPPO_DB)

def development():
    client = MongoClient("localhost", 27017)
    db = client.test_collection
    db.list_collection_names()
    imperatriz = db.test_db
    gs_imperatriz.start(imperatriz)


if __name__ == '__main__':
     production()
