import os

from greynoise import GreyNoise
from feeder import mongoHandler
from flask import jsonify


def get_ip(ip: str) -> (dict, dict):
    greynoise = GreyNoise(os.getenv('GN_API_KEY'))
    return greynoise.ip(ip), greynoise.metadata()


def quick_ip(ip: str) -> dict:
    greynoise = GreyNoise(os.getenv('GN_API_KEY'))
    return greynoise.quick(ip)


def build_tag_details(metadata, tags):
    detailed_tags = []
    for tag in tags:
        for detailed_tag in metadata["metadata"]:
            if tag == detailed_tag["name"]:
                detailed_tags.append(detailed_tag)
    return detailed_tags


def get_riot(ip: str) -> dict:
    greynoise = GreyNoise(os.getenv('GN_API_KEY'))
    return greynoise.riot(ip)


def process_ip(ip: str):
    if not mongoHandler.is_ip_in_greynoise(ip):
        gn_quick_data = quick_ip(ip)
        result = gn_quick_data[0]

        if result['riot']:
            gn_riot_data = get_riot(ip)
            return jsonify(gn_riot_data)

        if result['noise']:
            context_response, tags_response = get_ip(ip)
            updated_tags = build_tag_details(tags_response, context_response["tags"])
            context_response.pop("tags")
            context_response["tags"] = updated_tags
            mongoHandler.put_ip_in_greynoise(context_response)

            return jsonify(context_response)

    else:
        return jsonify(mongoHandler.get_ip_from_greynoise(ip))
