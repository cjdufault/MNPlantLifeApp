import requests
import re

gazetteer_url = "http://services.dnr.state.mn.us/api/gazetteer/v1?type=sna&name="
sna_detail_url = "http://services.dnr.state.mn.us/api/sna/detail/v1?id="


# searches the dnr gazetteer api for an sna matching an inputted string
def search(search_string):
    results = gazetteer_request(search_string)

    list_of_snas = []
    try:
        for result in results:
            list_of_snas.append(SNA(result))

    except TypeError:
        print("No results found for " + search_string)

    return list_of_snas


def gazetteer_request(search_string):
    response = requests.get(gazetteer_url + search_string).json()
    if response["status"] == "OK":
        results = response["results"]
        return results


# fills an SNA object in w/ all of the deets
def sna_details_request(sna):
    response = requests.get(sna_detail_url + sna.get_id()).json()

    if response["status"] == "SUCCESS":  # because apparently consistency is for chumps
        result = response["result"]

        sna.trees_shrubs = result["species"]["tree_shrub"]
        sna.grasses = result["species"]["grass_sedge"]
        sna.wildflowers = result["species"]["wildflower"]
        sna.desc = remove_html_tags(result["description"])
        sna.notes = remove_html_tags(result["notes"])
        sna.tags = result["tags"]
        sna.directions = remove_html_tags(result["parking"][0]["directions"])

        return sna


# some strings from the api have html tags in them. this removes them
def remove_html_tags(string):
    return re.sub(r"<[^<]+?>", "", string)  # found this regex here: https://stackoverflow.com/a/4869782


class SNA:
    def __init__(self, request_result):  # result is a json from the gazetteer api
        self.id = str.lower(request_result["id"])  # gazetteer has this w/ SNA in caps, but details wants it lower case
        self.coordinates_box = request_result["bbox"]["epsg:4326"]
        self.county = request_result["county"]
        self.name = request_result["name"]
        self.trees_shrubs = []
        self.grasses = []
        self.wildflowers = []
        self.desc = ""
        self.notes = ""
        self.tags = []
        self.directions = ""
