from flask import Flask, request, render_template, send_from_directory
import dnr_apis as dnr
import trefle_api as trefle
import os

app = Flask(__name__)
mapbox_token = os.environ.get("MAPBOX_TOKEN")
all_sna = dnr.search("")


@app.route("/")
def home():
    return render_template("home.html", list_heading="All MN Scientific & Natural Areas:", results=all_sna.keys())


# shows SNA search results
@app.route("/", methods=["POST"])
def sna_search():
    search_term = request.form["search"]
    results = dnr.search(search_term)

    return render_template("home.html", list_heading=f"Search Results for \"{search_term}\":",
                           search=search_term, results=results.keys())


# page that shows info on a specified SNA
@app.route("/sna/<sna_name>")
def sna_page(sna_name):
    try:
        try:
            sna_id = all_sna[sna_name]  # get id from existing search results
        except KeyError:
            sna_id = dnr.search(sna_name)[sna_name]  # if that fails, do a search again to get id

        sna = dnr.sna_details_request(sna_id)

        return render_template("sna_page.html", sna_object=sna, mapbox_token=mapbox_token)
    except KeyError:
        return f"<h1>No result found for \"{sna_name}\"</h1>\n" \
               f"<a href=\"/\">Return home</a>"


@app.route("/plant/<sci_name>")
def plant_page(sci_name):
    plant = trefle.search(sci_name)

    if plant is not None:
        return render_template("plant_page.html", plant_object=plant)
    else:
        return f"<h1>No result found for \"{sci_name}\"</h1>\n" \
               f"<a href=\"/\">Return home</a>"


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run()
