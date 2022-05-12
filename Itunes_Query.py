import requests
import json

iTunesURL = 'https://itunes.apple.com/search'
parameters = {"term": "Foro", "entity": "podcast"}

iTunes_response = requests.get("https://itunes.apple.com/search", params=parameters)

py_data = json.loads(iTunes_response.text)

# print('py_data type: ', type(py_data))
# print('py_data keys: ', list(py_data.keys()))
# print("py_data['results'] type: ", type(py_data['results']))
# print("py_data['results'] length: ", len(py_data['results']))
# print("py_data['results'][0] type: ", type(py_data['results'][0]))
# print("py_data['results'][0] keys: ", list(py_data['results'][0].keys()))

for result in py_data['results'][:4]:
    print(result['trackName'])