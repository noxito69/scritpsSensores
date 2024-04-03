import json
import uuid
from arreglo import Arreglo
from datetime import datetime

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
        return f"{self.tipo_sensor} (numero de serie:{self.numeroSerie}) (data:{self.data}) (fecha: ${self.fecha}) (hora: {self.hora} )"
        
    def dictionary(self):
        return{
            "uuid": str(self.uuid),  # Convertir UUID a cadena antes de serializarlo
            "tipo_sensor": self.tipo_sensor,
            "numero de serie": self.numeroSerie,
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
            dat = Data(data['tipo_sensor'], data['numero de serie'], data['data'])
            data_str += str(dat) + "\n"
            self.post(dat)
        
        return data_str.strip()

if __name__ == "__main__":
    x = Data()
    
    print(x.extract_data(x.extraer_json("data")))

    for func in x.arreglo:
        print("Data", type(func))

    F = Data("US", 1, "1195")
    E = Data("SIN",2,"horizontal")
    x.post(F)
    x.post(E)
    
    print(x.ConvertoJson())
