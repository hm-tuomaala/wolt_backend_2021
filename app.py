from flask import Flask, request, jsonify
from datetime import datetime
import json
import geopy.distance

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False

DATE_FORMAT = "%Y-%m-%d"


def calc_dist(c1_lat, c1_lon, c2_lat, c2_lon):
    c1 = (c1_lat, c1_lon)
    c2 = (c2_lat, c2_lon)
    return geopy.distance.distance(c1, c2).km


def month_diff(date_str):
    date = datetime.strptime(date_str, DATE_FORMAT)
    now = datetime.now()
    return (now.year - date.year) * 12 + now.month - date.month


def sort_newest(date_str):
    return (datetime.now() - datetime.strptime(date_str, DATE_FORMAT))


@app.route("/", methods = ['GET'])
def root():
    return "This is the root of the endpoint"


@app.route("/discovery", methods = ['GET'])
def search():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        # lat and/or lon query parameters are not of right type
        return (jsonify({"Error": "lat and lon type must be float"}), 400)
    except TypeError:
        # lat and/or lon query parameters are missing
        return (jsonify({"Error": "lat and lon values must be included in the query string"}), 400)

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
            if calc_dist(lat,lon, lat_restaurant, lon_restaurant) < 1.5:
                popular_restaurants["restaurants"].append(item)
                near_restaurants["restaurants"].append(item)
                if month_diff(item["launch_date"]) <= 4:
                    new_restaurants["restaurants"].append(item)

    # Sort popular restaurants first by online status and then by popularity
    sort_func = lambda x: (-x["online"], -x["popularity"])
    popular_restaurants["restaurants"] = sorted(popular_restaurants["restaurants"], key=sort_func)[:10]
    sort_func = lambda x: (-x["popularity"])
    popular_restaurants["restaurants"] = sorted(popular_restaurants["restaurants"], key=sort_func)

    # Sort new restaurants first by online status and then by launch_date
    sort_func = lambda x: (-x["online"], sort_newest(x["launch_date"]))
    new_restaurants["restaurants"] = sorted(new_restaurants["restaurants"], key=sort_func)[:10]
    sort_func = lambda x: (sort_newest(x["launch_date"]))
    new_restaurants["restaurants"] = sorted(new_restaurants["restaurants"], key=sort_func)

    # Sort nearby restaurants by online status and then by proximity
    sort_func = lambda x: (-x["online"], calc_dist(lat, lon, x["location"][1], x["location"][0]))
    near_restaurants["restaurants"] = sorted(near_restaurants["restaurants"], key=sort_func)[:10]
    sort_func = lambda x: (calc_dist(lat, lon, x["location"][1], x["location"][0]))
    near_restaurants["restaurants"] = sorted(near_restaurants["restaurants"], key=sort_func)

    if len(popular_restaurants["restaurants"]) > 0:
        ret["sections"].append(popular_restaurants)
    if len(new_restaurants["restaurants"]) > 0:
        ret["sections"].append(new_restaurants)
    if len(near_restaurants["restaurants"]) > 0:
        ret["sections"].append(near_restaurants)

    return jsonify(ret)

if __name__ == '__main__':
    app.run(debug=True)
