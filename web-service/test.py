import requests

house = {
    "City": "Kolkata",
    "Area Locality": "Bandel",
    "Tenant Preferred": "Bachelors",
    "BHK": 10,
    "Size": 1700
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=house)
print(response.json())
