from feeder import mongoHandler
import pymongo


def create_global_database():
    greynoise_ips = mongoHandler.get_greynoise_ips()
    feodo_ips = mongoHandler.get_feodo_ips()

    common_ips = [ip for ip in greynoise_ips if ip in feodo_ips]
