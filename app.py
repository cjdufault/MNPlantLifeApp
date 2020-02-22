from flask import Flask
import dnr_apis as dnr
import trefle_api as trefle

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
