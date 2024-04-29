import pymongo
import json
import requests
import time

def check_internet():
    url='http://www.google.com/'
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False

def save_to_mongodb(data):
    try:
       
        client = pymongo.MongoClient("mongodb://3.14.83.197:27117/")
        db = client["sensores"]
        col = db["data-sensores"]

       
        if isinstance(data, list):
            col.insert_many(data)
       
        else:
            col.insert_one(data)
        
        print("Los datos se han enviado correctamente a MongoDB.")
        return True

    except Exception as err:
        print("Ocurrió un error al enviar los datos a MongoDB: ", err)
        return False

def save_to_json(data):
    with open('isg.json', 'w') as f:
        json.dump(data, f)
    print("Los datos se han guardado en isg.json.")

def process_data():
    data = load_from_json()  
    for i in range(len(data)):
        if check_internet():
            if save_to_mongodb(data[i]):
                
                data.pop(i)
                save_to_json(data)
                break
        else:
            save_to_json(data)

def load_from_json():
    with open('isg.json', 'r') as f:
        data = json.load(f)
    return data


while True:
    process_data()
    time.sleep(1) 