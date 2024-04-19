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
        # Crea una conexión con MongoDB
        client = pymongo.MongoClient("mongodb://127.0.0.1:27117,127.0.0.1:27118/")
        db = client["sensores"]
        col = db["data-sensores"]

        # Si el archivo JSON contiene una lista de documentos
        if isinstance(data, list):
            col.insert_many(data)
        # Si el archivo JSON contiene un solo documento
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
    data = load_from_json()  # Carga los datos del archivo JSON
    for i in range(len(data)):
        if check_internet():
            if save_to_mongodb(data[i]):
                # Si los datos se enviaron a MongoDB con éxito, borra los datos del archivo JSON
                data.pop(i)
                save_to_json(data)
                break
        else:
            save_to_json(data)

def load_from_json():
    with open('isg.json', 'r') as f:
        data = json.load(f)
    return data

# Ejemplo de uso
while True:
    process_data()
    time.sleep(1)  # Espera 3 segundos antes de verificar de nuevo