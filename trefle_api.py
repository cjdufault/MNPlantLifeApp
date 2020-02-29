import requests
import os


token = os.environ.get("TREFLE_TOKEN")
trefle_url = "https://trefle.io/api/species"


def search(sci_name):
    try:
        result = species_request(sci_name)[0]
        plant = species_details_request(result)
        return plant
    except IndexError:
        print("No result found for " + sci_name)


def species_request(sci_name):
    request_url = trefle_url + "?token=" + token + "&scientific_name=" + sci_name
    response = requests.get(request_url)

    if response.status_code == 200:
        results = response.json()
        return results


def species_details_request(request_result):
    request_url = trefle_url + "/" + str(request_result["id"]) + "?token=" + token
    response = requests.get(request_url)

    if response.status_code == 200:
        result = response.json()
        plant = Plant(result)
        return plant


class Plant:
    def __init__(self, request_result):
        self.id = request_result["id"]
        self.common_name = request_result["common_name"]
        self.sci_name = request_result["scientific_name"]
        self.family = request_result["family_common_name"]
        self.toxicity = request_result["specifications"]["toxicity"]
        self.shape_orientation = request_result["specifications"]["shape_and_orientation"]

