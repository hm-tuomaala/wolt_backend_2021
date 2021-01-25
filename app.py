from flask import Flask, request, jsonify
from datetime import datetime
import json
import geopy.distance

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False

def calc_dist(c1_lat, c1_lon, c2_lat, c2_lon):
    c1 = (c1_lat, c1_lon)
    c2 = (c2_lat, c2_lon)
    return geopy.distance.distance(c1, c2).km


def month_diff(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    now = datetime.now()
    return (now.year - date.year) * 12 + now.month - date.month

def sort_newest(date_str):
    return (datetime.now() - datetime.strptime(date_str, "%Y-%m-%d"))

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
        # lat and/or lon query parameters are not of right type
        return "Error in query string: lat and lon type must be int or float"
    except TypeError:
        # lat and/or lon query parameters are missing
        return "Error in query parameters: you must include lat and lon values"

    ret = {
        "sections": []
    }

    popular_restaurants = {
        "title": "Popular Restaurants",
        "restaurants": []
    }

    new_restaurants = {
        "title": "New Restaurants",
        "restaurants": []
    }

    near_restaurants = {
        "title": "Nearby Restaurants",
        "restaurants": []
    }

    with open("restaurants.json", "r") as json_data:
        restaurants = json.load(json_data)
        for item in restaurants["restaurants"]:
            lat_restaurant = item["location"][1]
            lon_restaurant = item["location"][0]
            if calc_dist(lat,lon, lat_restaurant, lon_restaurant) <= 1.5:
                popular_restaurants["restaurants"].append(item)
                near_restaurants["restaurants"].append(item)
                if month_diff(item["launch_date"]) <= 4:
                    new_restaurants["restaurants"].append(item)

    # Sort popular restaurants first by online status and then by popularity
    popular_restaurants["restaurants"] = sorted(popular_restaurants["restaurants"], key=lambda x: (-x["online"], -x["popularity"]))[:10]

    # Sort new restaurants first by online status and then by launch_date
    new_restaurants["restaurants"] = sorted(new_restaurants["restaurants"], key=lambda x: (-x["online"], sort_newest(x["launch_date"])))[:10]

    near_restaurants["restaurants"] = sorted(near_restaurants["restaurants"], key=lambda x: (-x["online"], calc_dist(lat, lon, x["location"][1], x["location"][0])))

    ret["sections"].append(popular_restaurants)
    ret["sections"].append(new_restaurants)
    ret["sections"].append(near_restaurants)

    return jsonify(ret)

if __name__ == '__main__':
    app.run()
