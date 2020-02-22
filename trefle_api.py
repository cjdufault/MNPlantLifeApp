import requests
import os


token = os.environ.get("TREFLE_TOKEN")
trefle_url = "https://trefle.io/api/species?token=" + token + "&scientific_name="


def search(scientific_name):
    return species_request(scientific_name)


def species_request(scientific_name):
    response = requests.get(trefle_url + scientific_name).json()
    return response
