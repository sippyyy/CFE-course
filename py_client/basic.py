import requests

endpoint = "http://localhost:8000/api/"

get_response = requests.post(endpoint,json={"content":"content","price":"12.22"})
print(get_response.text)