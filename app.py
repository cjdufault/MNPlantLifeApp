from flask import Flask, request, render_template
import dnr_apis as dnr
import trefle_api as trefle

app = Flask(__name__)
search_results = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/", methods=["POST"])
def sna_search():
    search_term = request.form["search"]
    results = dnr.search(search_term)

    for result in results.keys():
        search_results[result] = results[result]

    return render_template("search_result.html", search=search_term, results=results)


@app.route("/sna/<sna_name>")
def sna_page(sna_name):
    try:
        sna_id = search_results[sna_name]  # get id from existing search results
    except KeyError:
        sna_id = dnr.search(sna_name)[sna_name]  # if that fails, do a search again to get id

    sna_object = dnr.sna_details_request(sna_id)

    return render_template("sna_page.html", name=sna_object.name, county=sna_object.county)


@app.route("/plant/<sci_name>")
def plant_page(sci_name):
    return sci_name


if __name__ == "__main__":
    app.run()
