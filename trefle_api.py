import requests
import os


token = os.environ.get("TREFLE_TOKEN")
trefle_url = "https://trefle.io/api/species"


def search(sci_name):
    try:
        result = species_request(sci_name)[0]
        plant = Plant(result)
        return plant
    except IndexError:
        print("No result found for " + sci_name)    # TODO: pass this to the UI in some way


def species_request(sci_name):
    request_url = trefle_url + "?token=" + token + "&scientific_name=" + sci_name
    response = requests.get(request_url)

    if response.status_code == 200:
        results = response.json()
        return results


def species_details_request(plant):
    species_id = plant.get_id()

    request_url = trefle_url + "/" + str(species_id) + "?token=" + token
    response = requests.get(request_url)

    if response.status_code == 200:
        result = response.json()
        return result   # TODO: map this result to attributes of the Plant class


class Plant:
    def __init__(self, request_result):
        self.id = request_result["id"]
        self.common_name = request_result["common_name"]
        self.sci_name = request_result["scientific_name"]

    def get_id(self): return self.id
    def get_common_name(self): return self.common_name
    def get_sci_name(self): return self.sci_name

    def set_id(self, new_id): self.id = new_id
    def set_common_name(self, new_common_name): self.common_name = new_common_name
    def set_sci_name(self, new_sci_name): self.sci_name = new_sci_name
