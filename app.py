from flask import Flask, request, render_template
import dnr_apis as dnr
import trefle_api as trefle

app = Flask(__name__)
search_results = {}


@app.route("/")
def home():
    return render_template("home.html")


# shows SNA search results
@app.route("/", methods=["POST"])
def sna_search():
    search_term = request.form["search"]
    results = dnr.search(search_term)

    for result in results.keys():
        search_results[result] = results[result]

    return render_template("search_result.html", search=search_term, results=results)


# page that shows info on a specified SNA
@app.route("/sna/<sna_name>")
def sna_page(sna_name):
    try:
        try:
            sna_id = search_results[sna_name]  # get id from existing search results
        except KeyError:
            sna_id = dnr.search(sna_name)[sna_name]  # if that fails, do a search again to get id

        sna_object = dnr.sna_details_request(sna_id)

        return render_template("sna_page.html",
                               name=sna_object.name,
                               tags=sna_object.tags,
                               county=sna_object.county,
                               desc=sna_object.desc,
                               notes=sna_object.notes,
                               directions=sna_object.directions,
                               wildflowers=sna_object.wildflowers,
                               grasses=sna_object.grasses,
                               trees_shrubs=sna_object.trees_shrubs)
    except KeyError:
        return f"<h1>No result found for \"{sna_name}\"</h1>\n" \
               f"<a href=\"/\">Return home</a>"


@app.route("/plant/<sci_name>")
def plant_page(sci_name):
    try:
        plant = trefle.search(sci_name)
        return render_template("plant_page.html",
                               cname=plant.common_name,
                               sname=plant.sci_name)
    except AttributeError:
        return f"<h1>No result found for \"{sci_name}\"</h1>\n" \
               f"<a href=\"/\">Return home</a>"


if __name__ == "__main__":
    app.run()
