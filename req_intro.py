import requests
import json

key = "pk.cbc1cf1b649ff5d37e57bf7445b43d16"
query = "Sinai Temple Los Angeles"
url = "https://us1.locationiq.com/v1/search?format=json&normalizeaddress=1&addressdetails=1"
headers = {"accept": "application/json"}

response = requests.get(url=f"{url}&key={key}&q={query}",headers=headers)
response_dict = {}

if str(response.status_code)[0] != "2":
    print(f"ERR: {response.status_code}")
else:
    reponse_dict = response.json()
    print(response_dict)

