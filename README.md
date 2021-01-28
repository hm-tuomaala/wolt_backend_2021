# wolt_backend_2021
This is my solution to the Wolt 2021 internship assignment developed
with python and flask.

### Prerequisites
* Python version 3.6 or newer

### Run development server
<sub><sup>_Use of virtualenv is advised_</sub></sup>\
In order to run Flask development server, `cd` into wolt_backend_2021 folder and run:  
`pip3 install -r requirements.txt`  
Then run:  
`python3 app.py`  
API endpoint will be running at: http://localhost:5000/discovery

### Tests
In order to run the test suite, `cd` into wolt_backend_2021 folder and run:  
`pytest`


### Usage
* You can query the API to find most popular, newest and nearby restaurants
(based on given coordinates)
* Example URI: _/discovery?lat=60.1709&lon=24.941_
