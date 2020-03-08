from flask import Flask, request, render_template, send_from_directory
import dnr_apis as dnr
import trefle_api as trefle
import os

app = Flask(__name__)
sna_ids = {}    # IDs to be referenced to get details on an SNA (sna_ids[{SNA name}] = {SNA_ID})
mapbox_token = os.environ.get("MAPBOX_TOKEN")


@app.route("/")
def home():
    all_sna = dnr.search("")

    for sna_name in all_sna.keys():  # grab all of the IDs for each SNA
        sna_ids[sna_name] = all_sna[sna_name]

    return render_template("home.html", list_heading="All MN Scientific & Natural Areas:", results=all_sna)


# shows SNA search results
@app.route("/", methods=["POST"])
def sna_search():
    search_term = request.form["search"]
    results = dnr.search(search_term)

    return render_template("home.html", list_heading=f"Search Results for \"{search_term}\":",
                           search=search_term, results=results)


# page that shows info on a specified SNA
@app.route("/sna/<sna_name>")
def sna_page(sna_name):
    try:
        try:
            sna_id = sna_ids[sna_name]  # get id from existing search results
        except KeyError:
            sna_id = dnr.search(sna_name)[sna_name]  # if that fails, do a search again to get id

        sna = dnr.sna_details_request(sna_id)

        return render_template("sna_page.html", sna_object=sna, mapbox_token=mapbox_token)
    except KeyError:
        return f"<h1>No result found for \"{sna_name}\"</h1>\n" \
               f"<a href=\"/\">Return home</a>"


@app.route("/plant/<sci_name>")
def plant_page(sci_name):
    try:
        plant = trefle.search(sci_name)
        return render_template("plant_page.html", plant_object=plant)
    except AttributeError:
        return f"<h1>No result found for \"{sci_name}\"</h1>\n" \
               f"<a href=\"/\">Return home</a>"


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico")


if __name__ == "__main__":
    app.run()
