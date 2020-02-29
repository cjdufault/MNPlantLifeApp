import trefle_api as trefle
import json

response = trefle.species_request("Betula pumila")
print(json.dumps(response, indent=4))
print()

plant = trefle.search("Betula pumila")
print(plant.id)
print(plant.common_name)
print(plant.sci_name)
print(plant.shape_orientation)
