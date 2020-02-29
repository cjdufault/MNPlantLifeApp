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
        self.mature_height_ft = request_result["specifications"]["mature_height"]["ft"]
        self.mature_height_cm = request_result["specifications"]["mature_height"]["cm"]
        self.lifespan = request_result["specifications"]["lifespan"]
        self.growth_rate = request_result["specifications"]["growth_rate"]
        self.growth_period = request_result["specifications"]["growth_period"]
        self.growth_habit = request_result["specifications"]["growth_habit"]
        self.growth_form = request_result["specifications"]["growth_form"]
        self.duration = request_result["duration"]  # e.g. annual, perennial, etc
        self.flower_color = request_result["flower"]["color"]
        self.foliage_color = request_result["foliage"]["color"]
        self.images = request_result["images"]  # urls of images of the plant
        self.temp_min_f = request_result["growth"]["temperature_minimum"]["deg_f"]
        self.temp_min_c = request_result["growth"]["temperature_minimum"]["deg_c"]
        self.shade_tolerance = request_result["growth"]["shade_tolerance"]
        self.salinity_tolerance = request_result["growth"]["salinity_tolerance"]
        self.root_depth_min_in = request_result["growth"]["root_depth_minimum"]["inches"]
        self.root_depth_min_cm = request_result["growth"]["root_depth_minimum"]["cm"]
        self.precip_min_in = request_result["growth"]["precipitation_minimum"]["inches"]
        self.precip_min_cm = request_result["growth"]["precipitation_minimum"]["cm"]
        self.precip_max_in = request_result["growth"]["precipitation_maximum"]["inches"]
        self.precip_max_cm = request_result["growth"]["precipitation_maximum"]["cm"]
        self.ph_min = request_result["growth"]["ph_minimum"]    # max acidity of soil
        self.ph_max = request_result["growth"]["ph_maximum"]    # max basicity of soil
        self.moisture_use = request_result["growth"]["moisture_use"]
        self.fire_tolerance = request_result["growth"]["fire_tolerance"]
        self.drought_tolerance = request_result["growth"]["drought_tolerance"]
        self.anaerobic_tolerance = request_result["growth"]["anaerobic_tolerance"]
