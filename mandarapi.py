import json
import requests
import time

while True:
    
    with open('isg.json', 'r') as file:
        data = json.load(file)

   
    url = 'http://192.168.137.51:8000/api/guardardatos'

    if data:  
       
        response = requests.post(url, json=data)
        print(response.status_code)
        print(response.text)
       
        with open('isg.json', 'w') as file:
            file.write(json.dumps([]))
    
    time.sleep(6)
