from flask import Flask, request, render_template
import dnr_apis as dnr
import trefle_api as trefle
import os

app = Flask(__name__)
mapbox_token = os.environ.get("MAPBOX_TOKEN")

all_sna = dnr.sna_list_request()
all_sna_keys = list(all_sna.keys())
all_sna_keys.sort()


@app.route("/")
def home():
    # so that if the dict of SNAs changes while the site is up, it will be updated when the site is accessed
    load_sna_list()

    return render_template("home.html", list_heading="All MN Scientific & Natural Areas:", results=all_sna_keys)


# shows SNA search results
@app.route("/", methods=["POST"])
def sna_search():
    search_term = request.form["search"]
    results = search(search_term)

    return render_template("home.html", list_heading=f"Search Results for \"{search_term}\":",
                           search=search_term, results=results)


# page that shows info on a specified SNA
@app.route("/sna/<sna_name>")
def sna_page(sna_name):
    try:
        try:
            sna_id = all_sna[sna_name]  # get id from existing search results
        except KeyError:
            # maybe they didn't input it with correct capitalization
            formatted_name = str.title(sna_name).replace(" Sna", " SNA")

            if " SNA" not in formatted_name:
                formatted_name = formatted_name + " SNA"

            sna_id = all_sna[formatted_name]

        sna = dnr.sna_details_request(sna_id)

        return render_template("sna_page.html", sna_object=sna, mapbox_token=mapbox_token)
    except KeyError:
        return f"<h1>No result found for \"{sna_name}\"</h1>\n" \
               f"<a href=\"/\">Return home</a>"


@app.route("/plant")
def plant_page():
    sci_name = request.args.get("sci_name", type=str)
    common_name = request.args.get("common_name", type=str)

    if sci_name is None:
        return f"<h1>No scientific name provided</h1>\n" \
               f"<a href=\"/\">Return home</a>"

    plant = trefle.search(sci_name)

    if plant is None and common_name is not None:
        # sometimes the value for sci name is actually the common name due to data entry errors
        print("Retrying search with common name as scientific name")
        plant = trefle.search(common_name)

    if plant is not None:
        print("Success! Common and scientific names were switched.")
        return render_template("plant_page.html", plant_object=plant)
    else:
        print(f"Could not find data for {sci_name}")
        return f"<h1>No result found for \"{sci_name}\"</h1>\n" \
               f"<a href=\"/\">Return home</a>"


@app.route("/about")
def about():
    return render_template("about.html")


def search(search_string):
    matches = []

    for sna in all_sna_keys:
        if str.lower(search_string) in str.lower(sna):
            matches.append(sna)

    return matches


def load_sna_list():
    global all_sna
    global all_sna_keys

    all_sna = dnr.sna_list_request()
    all_sna_keys = list(all_sna.keys())
    all_sna_keys.sort()


if __name__ == "__main__":
    app.run()
