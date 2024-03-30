from typing import Any, Mapping, List, Type

import pymongo
import json
import os
from flask import jsonify
from pymongo.cursor import Cursor


def is_ip_in_greynoise(ip: str) -> bool:
    client = pymongo.MongoClient(os.getenv('MONGO_URI'))
    db = client['threatpulse']
    collection = db['greynoise_ips']
    return bool(collection.find_one({'ip': ip}))


def put_ip_in_greynoise(ip: str) -> bool:
    client = pymongo.MongoClient(os.getenv('MONGO_URI'))
    db = client['threatpulse']
    collection = db['greynoise_ips']
    collection.update_one({'ip': ip['ip']}, {'$set': json.loads(json.dumps(ip))}, upsert=True)


def get_ip_from_greynoise(ip: str) -> dict:
    client = pymongo.MongoClient(os.getenv('MONGO_URI'))
    db = client['threatpulse']
    collection = db['greynoise_ips']
    document = collection.find_one({'ip': ip})

    if document and '_id' in document:
        del document['_id']

    return document


def get_collection_ips(collection_name) -> list[Any]:
    client = pymongo.MongoClient(os.getenv('MONGO_URI'))
    db = client['threatpulse']
    collection = db[collection_name]

    ips = collection.find({}, projection={'ip': 1})
    list_ips = list()
    for ip in ips:
        list_ips.append(ip['ip'])

    return list_ips


def get_greynoise_ips() -> list[Any]:
    return get_collection_ips('greynoise_ips')


def get_feodo_ips() -> list[Any]:
    return get_collection_ips('feodo_c2s')


def put_ioc_in_threatfox(ioc: dict):
    client = pymongo.MongoClient(os.getenv('MONGO_URI'))
    db = client['threatpulse']
    collection = db['threatfox_iocs']

    collection.update_one({'ioc': ioc['ioc']}, {'$set': json.loads(json.dumps(ioc))}, upsert=True)
