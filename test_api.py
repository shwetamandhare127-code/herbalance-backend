import requests

url = "http://127.0.0.1:5000/predict"

data = {
    "username": "Shweta",
    "age": 25,
    "weight": 70,
    "bmi": 28,
    "cycle_length": 40,
    "hair_growth": 1,
    "skin_darkening": 1,
    "pimples": 1,
    "weight_gain": 1,
    "fast_food": 1,
    "exercise": 0
}

response = requests.post(url, json=data)

print(response.json())