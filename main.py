"""
curl -X 'POST' \
  'http://5.63.153.31:5051/v1/account' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "login": "u2",
  "email": "test@test2.de",
  "password": "123456789"
}'
curl -X 'PUT' \
  'http://5.63.153.31:5051/v1/account/fc5c9258-0e89-4d18-8f5d-aabbb4d5e05e' \
  -H 'accept: text/plain'
"""
import pprint
from http.client import responses

import requests

#url = 'http://5.63.153.31:5051/v1/account'
#headers = {
 #   'accept': '*/*',
 #   'Content-Type': 'application/json',

#}
#json = {
    #"login": "u2",
   # "email": "test@test2.de",
   # "password": "123456789"
#}
#response = requests.post(
  #  url=url,
  #  headers=headers,
   # json=json
#)
url = 'http://5.63.153.31:5051/v1/account/fc5c9258-0e89-4d18-8f5d-aabbb4d5e05e'
headers = {
    'accept': 'text/plain'

}

response = requests.put(
    url=url,
    headers=headers,

)
print(response.status_code)
pprint.pprint(response.json())
response_json = response.json()
print(response_json['resource']['rating']['quantity'])
