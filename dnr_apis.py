import requests

gazetteer_url = "http://services.dnr.state.mn.us/api/gazetteer/v1?type=sna&name="
sna_detail_url = "http://services.dnr.state.mn.us/api/sna/detail/v1?id=%s"
sna_list_url = "http://services.dnr.state.mn.us/api/sna/list/v1"


def sna_search(name):
    gazetteer_response = requests.get(gazetteer_url + name).json()

    if gazetteer_response["status"] == "OK":
        gazetteer_results = gazetteer_response["results"]

        search_results = []    # list of the SNA objects created from the response
        for result in gazetteer_results:
            search_results.append(SNA(result))

        return search_results


class SNA:
    def __init__(self, result):     # result is a json from the gazetteer api
        self.id = result["id"]
        self.coordinates_box = result["bbox"]["epsg:4326"]
        self.county = result["county"]
        self.name = result["name"]
