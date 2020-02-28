import requests
import re

gazetteer_url = "http://services.dnr.state.mn.us/api/gazetteer/v1?type=sna&name="
sna_detail_url = "http://services.dnr.state.mn.us/api/sna/detail/v1?id="


# searches the dnr gazetteer api for an sna matching an inputted string
def search(search_string):
    results = gazetteer_request(search_string)

    sna_dict = {}
    try:
        for result in results:
            name = result["name"]
            sna_id = str.lower(result["id"])
            sna_dict[name] = sna_id

    except TypeError:
        print("No results found for " + search_string)

    return sna_dict


def gazetteer_request(search_string):
    response = requests.get(gazetteer_url + search_string).json()
    if response["status"] == "OK":
        results = response["results"]
        return results


# fills an SNA object in w/ all of the deets
def sna_details_request(sna_id):
    response = requests.get(sna_detail_url + sna_id).json()

    if response["status"] == "SUCCESS":  # because apparently consistency is for chumps
        request_result = response["result"]

        sna = (SNA(request_result))

        sna.trees_shrubs = request_result["species"]["tree_shrub"]
        sna.grasses = request_result["species"]["grass_sedge"]
        sna.wildflowers = request_result["species"]["wildflower"]
        sna.desc = remove_html_tags(request_result["description"])
        sna.notes = remove_html_tags(request_result["notes"])
        sna.tags = request_result["tags"]
        sna.directions = remove_html_tags(request_result["parking"][0]["directions"])

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
        self.directions = remove_html_tags(request_result["parking"][0]["directions"])
