import requests
import pymongo
import os


def get_feodo_c2s():
    r = requests.get('https://feodotracker.abuse.ch/downloads/ipblocklist_recommended.json')
    if r.status_code == 200:

        client = pymongo.MongoClient(os.getenv('MONGO_URI'))
        db = client["threatpulse"]
        collection = db["feodo_c2s"]

        for c2 in r.json():

            # $rename operator to cause some bugs or WriteError message ; do the job by hand :)
            # -> incompatibility with upserting ?
            ip = c2['ip_address']
            del c2['ip_address']
            c2['ip'] = ip

            collection.update_one({'ip': c2['ip']}, {
                '$set': c2,
            }, upsert=True)
