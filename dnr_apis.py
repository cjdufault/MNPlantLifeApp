import requests
import re

sna_list_url = "http://services.dnr.state.mn.us/api/sna/list/v1/"
sna_detail_url = "http://services.dnr.state.mn.us/api/sna/detail/v1?id="


def sna_list_request():
    response = requests.get(sna_list_url)

    if response.status_code == 200 and response.json()["status"] == "SUCCESS":
        sna_dict = {}
        results = response.json()["result"]

        for result in results:
            name = result["name"]
            sna_id = result["id"]
            sna_dict[name] = sna_id

        return sna_dict


# fills an SNA object in w/ all of the deets
def sna_details_request(sna_id):
    response = requests.get(sna_detail_url + sna_id)

    if response.status_code == 200 and response.json()["status"] == "SUCCESS":
        request_result = response.json()["result"]

        sna = (SNA(request_result))
        return sna


# some strings from the api have html tags in them. this removes them
def remove_html_tags(string):
    return re.sub(r"<[^<]+?>", "", string)  # found this regex here: https://stackoverflow.com/a/4869782


class SNA:
    def __init__(self, request_result):  # result is a json from the gazetteer api
        self.id = request_result["id"]
        self.coordinates_box = request_result["bbox"]["epsg:4326"]
        self.county = request_result["county"]
        self.name = request_result["name"]
        self.trees_shrubs = request_result["species"]["tree_shrub"]
        self.grasses = request_result["species"]["grass_sedge"]
        self.wildflowers = request_result["species"]["wildflower"]
        self.desc = remove_html_tags(request_result["description"])
        self.notes = remove_html_tags(request_result["notes"])
        self.tags = request_result["tags"]
        self.parking_longitude = request_result["parking"][0]["point"]["epsg:4326"][0]
        self.parking_latitude = request_result["parking"][0]["point"]["epsg:4326"][1]
        self.directions = remove_html_tags(request_result["parking"][0]["directions"])
