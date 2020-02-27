from flask import Flask, request, render_template
import dnr_apis as dnr
import trefle_api as trefle

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/', methods=["POST"])
def sna_search():
    search = request.form["search"]
    print(search)
    return render_template("search_result.html", search_term=search)


if __name__ == '__main__':
    app.run()
