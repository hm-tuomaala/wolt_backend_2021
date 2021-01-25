from flask import Flask, request
from datetime import datetime
import json
import geopy.distance

app = Flask(__name__)

def calc_dist(c1_lat, c1_lon, c2_lat, c2_lon):
    c1 = (c1_lat, c1_lon)
    c2 = (c2_lat, c2_lon)
    return geopy.distance.distance(c1, c2).km


def month_diff(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    now = datetime.now()
    return (now.year - date.year) * 12 + now.month - date.month

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

    

    print(popular_restaurants)
    print(new_restaurants)
    print(near_restaurants)

    return ret

if __name__ == '__main__':
    app.run()
