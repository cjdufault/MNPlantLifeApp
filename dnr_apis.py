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
            list_of_snas.append(result)

    except TypeError:
        print("No results found")

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

        sna.set_trees_shrubs(result["species"]["tree_shrub"])
        sna.set_grasses(result["species"]["grass_sedge"])
        sna.set_wildflowers(result["species"]["wildflower"])
        sna.set_desc(result["description"])
        sna.set_notes(result["notes"])
        sna.set_tags(result["tags"])
        sna.set_directions(result["parking"][0]["directions"])

        return sna


# some strings from the api have html tags in them. this removes them
def remove_html_tags(string):
    return re.sub(r"<[^<]+?>", "", string)  # found this regex here: https://stackoverflow.com/a/4869782


class SNA:
    def __init__(self, result):  # result is a json from the gazetteer api
        self.id = str.lower(result["id"])  # gazetteer returns this w/ SNA in caps, but details api wants it lower case
        self.coordinates_box = result["bbox"]["epsg:4326"]
        self.county = result["county"]
        self.name = result["name"]
        self.trees_shrubs = []
        self.grasses = []
        self.wildflowers = []
        self.desc = ""
        self.notes = ""
        self.tags = []
        self.directions = ""

    def get_id(self): return self.id
    def get_coordinates_box(self): return self.coordinates_box
    def get_county(self): return self.county
    def get_name(self): return self.name
    def get_trees_shrubs(self): return self.trees_shrubs
    def get_grasses(self): return self.grasses
    def get_wildflowers(self): return self.wildflowers
    def get_desc(self): return self.desc
    def get_notes(self): return self.notes
    def get_tags(self): return self.tags
    def get_directions(self): return self.directions

    def set_id(self, new_id): self.id = new_id
    def set_coordinates_box(self, new_coordinates_box): self.coordinates_box = new_coordinates_box
    def set_county(self, new_county): self.county = new_county
    def set_name(self, new_name): self.name = new_name
    def set_trees_shrubs(self, new_trees_shrubs): self.trees_shrubs = new_trees_shrubs
    def set_grasses(self, new_grasses): self.grasses = new_grasses
    def set_wildflowers(self, new_wildflowers): self.wildflowers = new_wildflowers
    def set_desc(self, new_desc): self.desc = remove_html_tags(new_desc)
    def set_notes(self, new_notes): self.notes = remove_html_tags(new_notes)
    def set_tags(self, new_tags): self.tags = new_tags
    def set_directions(self, new_directions): self.directions = remove_html_tags(new_directions)
