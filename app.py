from flask import Flask, request
import json

app = Flask(__name__)


@app.route("/")
def hello():
    return "This is the root of the endpoint"

@app.route("/discovery")
def endpoint():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return "Error in query string: lat and lon type must be int or float"
    except TypeError:
        # Either lat and/or lon query parameters are missing
        return "Error in query parameters: you must include lat and lon values"

    with open("restaurants.json", "r") as json_data:
        restaurants = json.load(json_data)
        print(restaurants)

    return "endpoint"

if __name__ == '__main__':
    app.run()
