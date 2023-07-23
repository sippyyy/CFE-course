import requests

endpoint = "http://localhost:8000/api/products/1/update/"

data ={"title": "Update Thuy"}
get_response = requests.put(endpoint,json=data)
print(get_response.json())