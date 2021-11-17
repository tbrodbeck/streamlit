from decouple import AutoConfig
import requests
import json
import ibm_db_py3
# config params
config = AutoConfig(search_path='./ds-bootcamp-mvp')
API_KEY=config('API_KEY')
ENDPOINT=config('ENDPOINT')
token_response = requests.post('https://iam.cloud.ibm.com/identity/token',
                               data={"apikey": API_KEY,
                                     "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'}
                               )
mltoken = token_response.json()["access_token"]

# to create header
header = {
'Authorization': 'Bearer  ' + mltoken}
data = {
'input_data': {
    'fields': ['title'],
    'values': [['Toy Story (1995)']]}
}

r = requests.post(ENDPOINT, headers=header, json=json.dumps(data))


# connection to db
conn_string = f"DATABASE={config('DB_NAME')};HOSTNAME={condig('DB_HOST')}" \
              f";PORT={config('DB_PORT')};PROTOCOL=TCPIP;UID={config('DB_USERNAME')};PWD={config('DB_PASSWORD')}"

conn = ibm_db.connect(conn_string)

class BasicModel:
  def __init__(self, param1, param2):
    self.param1 = param1
    self.param2 = param2

  def predict(inputs):
    # here to write a method
