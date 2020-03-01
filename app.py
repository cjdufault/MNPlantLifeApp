from flask import Flask, request, render_template, send_from_directory
import dnr_apis as dnr
import trefle_api as trefle
import os

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
                               name=sna_object.name, tags=sna_object.tags, county=sna_object.county,
                               desc=sna_object.desc, notes=sna_object.notes, directions=sna_object.directions,
                               wildflowers=sna_object.wildflowers, grasses=sna_object.grasses,
                               trees_shrubs=sna_object.trees_shrubs)
    except KeyError:
        return f"<h1>No result found for \"{sna_name}\"</h1>\n" \
               f"<a href=\"/\">Return home</a>"


@app.route("/plant/<sci_name>")
def plant_page(sci_name):
    try:
        plant = trefle.search(sci_name)
        return render_template("plant_page.html",
                               cname=plant.common_name, sname=plant.sci_name, images=plant.images, family=plant.family,
                               toxicity=plant.toxicity, shape=plant.shape_orientation,
                               mature_height_ft=plant.mature_height_ft, mature_height_cm=plant.mature_height_cm,
                               lifespan=plant.lifespan, growth_rate=plant.growth_rate,
                               growth_period=plant.growth_period, growth_habit=plant.growth_habit,
                               growth_form=plant.growth_form, duration=plant.duration, flower_color=plant.flower_color,
                               foliage_color=plant.foliage_color, temp_min_f=plant.temp_min_f,
                               temp_min_c=plant.temp_min_c, shade_tolerance=plant.shade_tolerance,
                               salinity_tolerance=plant.salinity_tolerance, root_depth_min_in=plant.root_depth_min_in,
                               root_depth_min_cm=plant.root_depth_min_cm, precip_min_in=plant.precip_min_in,
                               precip_min_cm=plant.precip_min_cm, precip_max_in=plant.precip_max_in,
                               precip_max_cm=plant.precip_max_cm, ph_min=plant.ph_min, ph_max=plant.ph_max,
                               moisture_use=plant.moisture_use, fire_tolerance=plant.fire_tolerance,
                               drought_tolerance=plant.drought_tolerance, anaerobic_tolerance=plant.anaerobic_tolerance)
    except AttributeError:
        return f"<h1>No result found for \"{sci_name}\"</h1>\n" \
               f"<a href=\"/\">Return home</a>"


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico")


if __name__ == "__main__":
    app.run()
