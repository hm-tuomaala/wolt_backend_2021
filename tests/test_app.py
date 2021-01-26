import requests
import pytest

def test_get_root_check_status_code_equals_200(client):
    # TODO: Complete the test here
    assert client.get("/").status_code == 200
