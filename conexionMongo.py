import pymongo
import json

# Crea una conexión con MongoDB
client = pymongo.MongoClient("mongodb+srv://erik:Erik0604@cluster0.pjaaz3u.mongodb.net/")

# Crea una nueva base de datos llamada "mydatabase"
db = client["sensores"]

# Crea una nueva colección llamada "mycollection"
col = db["data"]

# Abre y carga el archivo JSON
with open('data.json') as f:
    data = json.load(f)

# Si el archivo JSON contiene una lista de documentos
if isinstance(data, list):
    col.insert_many(data)
# Si el archivo JSON contiene un solo documento
else:
    col.insert_one(data)