import json
import uuid
from arreglo import Arreglo
from datetime import datetime
from comSerial import ComSerial

class Data(Arreglo):
    
    def __init__(self, tipo_sensor=None, numeroSerie=None, data=None):
        self.tipo_sensor = tipo_sensor
        self.numeroSerie = numeroSerie
        self.data = data
        self.fecha = datetime.now().strftime("%d-%m-%Y")  # Fecha actual en formato dd-mm-yyyy
        self.hora = datetime.now().strftime("%H:%M:%S")    # Hora actual en formato HH:MM:SS
        self.uuid = uuid.uuid4()  # Generar UUID único
     
        super().__init__()
         
    def __str__(self) -> str:
        return f"{self.tipo_sensor} (numero_serie:{self.numeroSerie}) (data:{self.data}) (fecha: ${self.fecha}) (hora: {self.hora} )"
        
    def dictionary(self):
        return{
            "uuid": str(self.uuid),  # Convertir UUID a cadena antes de serializarlo
            "tipo_sensor": self.tipo_sensor,
            "numero_serie": self.numeroSerie,
            "data": self.data,
            "fecha": self.fecha,
            "hora": self.hora,
        }
        
    def ConvertoJson(self):
        da = [x.dictionary() for x in self.arreglo]
        with open("./data.json", "w") as archivo:
            archivo.write(json.dumps(da, indent=2))
            
    def extract_data(self, json_data):
        data_str = ""
        for data in json_data:
            dat = Data(data['tipo_sensor'], data['numero_serie'], data['data'])
            data_str += str(dat) + "\n"
            self.post(dat)
        
        return data_str.strip()

    # agregué este de aqui para tomar los datos de mi ComSerial
    def procesar_datos(self, datos):
        for dato in datos:
            partes = dato.split('-')
            if len(partes) == 4:
                tipo_sensor, _, numeroSerie, data = partes
                self.tipo_sensor = tipo_sensor
                self.numeroSerie = numeroSerie
                self.data = data
                self.guardar_json() 

if __name__ == "__main__":
    x = ComSerial()
    '''datos = x.datoSerial()  # recupera los datos de ComSerial

    arreglo = Arreglo()  # instancia de arreglo

    datos_existentes = arreglo.extraer_json('data')

    for dato in datos:
        partes = dato.split('-')
        if len(partes) == 4:
            tipo_sensor, _, numeroSerie, data = partes
            d = Data(tipo_sensor, numeroSerie, data)
            arreglo.post(d)
    
    datos_json = []
    for item in arreglo.arreglo:
        item_dict = item.__dict__
        item_dict.pop('arreglo', None)  # Elimina el campo 'arreglo'
        # Asegúrate de que 'uuid' sea el primer campo
        item_dict = {'uuid': item_dict['uuid'], **item_dict}

        datos_json.append(item_dict)

    # Agrega los nuevos datos a los datos existentes
    datos_existentes.extend([item.__dict__ for item in arreglo.arreglo])
    
    # para guardarlo en el json con el formato
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump([item.__dict__ for item in arreglo.arreglo], file, default=str, ensure_ascii=False, indent=4)'''



    # LO DE ERIC
    
    
    
 #hola, esto es un ciclo que crea 10 registros de data nomas de prueba para mandarlos a mongo, puedes comentarlos cuando hagas las pruebas con el serial.
x = Data()

#print(x.extract_data(x.extraer_json("data")))

#for func in x.arreglo:
#    print("Data", type(func))

#for i in range(10):
#    F = Data("US", i, "1195")
#    E = Data("SIN", i, "horizontal")
#    x.post(F)
#    x.post(E)

#print(x.ConvertoJson())
'''d = x.extract_data(x.extraer_json("data"))

for func in x.arreglo:
    print("Data", type(func))

for i in range(10):
    F = Data("US", i, "1195")
    E = Data("SIN", i, "horizontal")
    x.post(F)
    x.post(E)
   

# Delete all records in the JSON file
#x.arreglo.clear()
x.ConvertoJson()
'''
