from feeder import mongoHandler
import requests
import pymongo
import os


def get_ioc_from_ip(ip: str) -> dict | None:

    url = "https://threatfox-api.abuse.ch/api/v1/"
    data = {
        "query": "search_ioc",
        "search_term": ip
    }

    response = requests.post(url, json=data)
    if response.status_code == 200:
        if response.json()['query_status'] == "ok":
            return response.json()['data']
        else:
            return None


def put_iocs_from_ip(ip: str) -> None:
    iocs = get_ioc_from_ip(ip)

    if iocs is not None:
        for ioc in iocs:
            mongoHandler.put_ioc_in_threatfox(ioc)


def enrich_from_threatfox():

    ips = mongoHandler.get_greynoise_ips()

    for ip in ips:
        ip = ip['ip']

        ioc = get_ioc_from_ip(ip)
        if ioc is not None:
            mongoHandler.put_ioc_in_threatfox(ioc)
