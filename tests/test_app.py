from app import calc_dist
from app import month_diff
from app import DATE_FORMAT
import requests
import pytest
from datetime import datetime


def test_get_status_code_with_valid_query_string(client):
    assert client.get("/discovery?lat=60.1709&lon=24.941").status_code == 200


def test_post_status_code(client):
    assert client.post("/discovery?lat=60.1709&lon=24.941").status_code == 405


def test_status_code_with_invalid_query_string_type(client):
    assert client.get("/discovery?lat=60.1709&lon=test").status_code == 400


def test_status_code_with_defective_query_string(client):
    assert client.get("/discovery?lat=60.1709").status_code == 400


def test_response_type(client):
    assert client.get("/discovery?lat=60.1709&lon=24.941").content_type == "application/json"


def test_response_sections(client):
    sections = client.get("/discovery?lat=60.1709&lon=24.941").json["sections"]
    section_titles = ["Popular Restaurants", "New Restaurants", "Nearby Restaurants"]
    for sec in sections:
        assert sec["title"] in section_titles


def test_response_empty_sections(client):
    assert client.get("/discovery?lat=65.1709&lon=28.941").json["sections"] == []


def test_response_section_lengths(client):
    sections = client.get("/discovery?lat=60.1709&lon=24.941").json["sections"]
    for sec in sections:
        assert len(sec["restaurants"]) == 10


def test_response_restaurants_closer_than_1500m(client):
    lat = 60.1709
    lon = 24.941
    sections = client.get(f"/discovery?lat={lat}&lon={lon}").json["sections"]
    for sec in sections:
        for restaurant in sec["restaurants"]:
            assert calc_dist(lat, lon, restaurant["location"][1], restaurant["location"][0]) < 1.5


def test_popular_restaurants_sorting(client):
    section1 = client.get("/discovery?lat=60.1709&lon=24.941").json["sections"]
    section2 = client.get("/discovery?lat=60.1579&lon=24.961").json["sections"]
    section3 = client.get("/discovery?lat=60.1630&lon=24.976").json["sections"]

    prev_popularity = 1.1
    for sec in section1:
        if sec["title"] == "Popular Restaurants":
            for restaurant in sec["restaurants"]:
                assert restaurant["popularity"] <= prev_popularity
                prev_popularity = restaurant["popularity"]

    prev_popularity = 1.1
    for sec in section2:
        if sec["title"] == "Popular Restaurants":
            for restaurant in sec["restaurants"]:
                assert restaurant["popularity"] <= prev_popularity
                prev_popularity = restaurant["popularity"]

    prev_popularity = 1.1
    for sec in section3:
        if sec["title"] == "Popular Restaurants":
            for restaurant in sec["restaurants"]:
                assert restaurant["popularity"] <= prev_popularity
                prev_popularity = restaurant["popularity"]


def test_new_restaurants_sorting(client):
    section1 = client.get("/discovery?lat=60.1709&lon=24.941").json["sections"]
    section2 = client.get("/discovery?lat=60.1579&lon=24.961").json["sections"]
    section3 = client.get("/discovery?lat=60.1630&lon=24.976").json["sections"]

    prev_date = datetime.now()
    for sec in section1:
        if sec["title"] == "New Restaurants":
            for restaurant in sec["restaurants"]:
                launch_date = datetime.strptime(restaurant["launch_date"], DATE_FORMAT)
                assert launch_date <= prev_date
                prev_date = launch_date

    prev_date = datetime.now()
    for sec in section2:
        if sec["title"] == "New Restaurants":
            for restaurant in sec["restaurants"]:
                launch_date = datetime.strptime(restaurant["launch_date"], DATE_FORMAT)
                assert launch_date <= prev_date
                prev_date = launch_date

    prev_date = datetime.now()
    for sec in section3:
        if sec["title"] == "New Restaurants":
            for restaurant in sec["restaurants"]:
                launch_date = datetime.strptime(restaurant["launch_date"], DATE_FORMAT)
                assert launch_date <= prev_date
                prev_date = launch_date


def test_nearby_restaurants_sorting(client):
    lat1 = 60.1709
    lon1 = 24.941
    section1 = client.get(f"/discovery?lat={lat1}&lon={lon1}").json["sections"]
    lat2 = 60.1579
    lon2 = 24.961
    section2 = client.get(f"/discovery?lat={lat2}&lon={lon2}").json["sections"]
    lat3 = 60.1630
    lon3 = 24.976
    section3 = client.get(f"/discovery?lat={lat3}&lon={lon3}").json["sections"]

    prev_dist = 0
    for sec in section1:
        if sec["title"] == "Nearby Restaurants":
            for restaurant in sec["restaurants"]:
                dist = calc_dist(lat1, lon1, restaurant["location"][1], restaurant["location"][0])
                assert dist >= prev_dist
                prev_dist = dist

    prev_dist = 0
    for sec in section2:
        if sec["title"] == "Nearby Restaurants":
            for restaurant in sec["restaurants"]:
                dist = calc_dist(lat2, lon2, restaurant["location"][1], restaurant["location"][0])
                assert dist >= prev_dist
                prev_dist = dist

    prev_dist = 0
    for sec in section3:
        if sec["title"] == "Nearby Restaurants":
            for restaurant in sec["restaurants"]:
                dist = calc_dist(lat3, lon3, restaurant["location"][1], restaurant["location"][0])
                assert dist >= prev_dist
                prev_dist = dist
