def get_history_databases():
    return [
         {
         "name": "fort",
         "collection": "history_fort"
         },
         {
         "name": "bistek",
         "collection": "history_bistek"
         },
         {
         "name": "imperatriz",
         "collection": "history_imperatriz"
         },
         # {
         # "name": "hippo",
         # "collection": "history_hippo"
         # },
    ]
def get_price_databases():
     return [
         {
         "name": "fort",
         "collection": "fort"
         },
         {
         "name": "bistek",
         "collection": "bistek"
         },
         {
             "name": "imperatriz",
             "collection": "imperatriz"
         },
         # {
         # "name": "hippo",
         # "collection": "hippo"
         # }
     ]

def get_history_database_by_name(name):
    dbs = get_history_databases()
    for db in dbs:
        if name in db.values():
            return db["collection"]
    return "Name not found"