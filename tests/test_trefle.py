import trefle_api as trefle
import json

response = trefle.search("Betula pumila")
print(json.dumps(response, indent=4))
