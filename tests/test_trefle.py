import trefle_api as trefle
import json

response = trefle.species_request("Betula pumila")
print(json.dumps(response, indent=4))
print()

plant = trefle.search("Betula pumila")
print(plant.get_id())
print(plant.get_common_name())
print(plant.get_sci_name())
print()

details_response = trefle.species_details_request(plant)
print(json.dumps(details_response, indent=4))
