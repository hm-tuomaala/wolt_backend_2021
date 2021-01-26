import requests
import pytest

def test_get_root_status_code(client):
    assert client.get("/").status_code == 200

def test_get_discovery_status_code_with_valid_query_string(client):
    assert client.get("/discovery?lat=60.1709&lon=24.941").status_code == 200

def test_get_discovery_status_code_with_invalid_query_string_type(client):
    assert client.get("/discovery?lat=60.1709&lon=test").status_code == 400

def test_get_discovery_status_code_with_defective_query_string(client):
    assert client.get("/discovery?lat=60.1709").status_code == 400

def test_get_discovery_response_type(client):
    assert client.get("/discovery?lat=60.1709&lon=24.941").content_type == "application/json"

def test_get_discovery_response_sections(client):
    sections = client.get("/discovery?lat=60.1709&lon=24.941").json["sections"]
    section_titles = ["Popular Restaurants", "New Restaurants", "Nearby Restaurants"]
    for sec in sections:
        assert sec["title"] in section_titles

def test_get_discovery_response_empty_sections(client):
    assert client.get("/discovery?lat=65.1709&lon=28.941").json["sections"] == []

def test_get_discovery_response_section_lengths(client):
    sections = client.get("/discovery?lat=60.1709&lon=24.941").json["sections"]
    for sec in sections:
        assert len(sec["restaurants"]) == 10
