from isf import ISF
from data import Data
from arreglo import Arreglo
import json
from comSerial import ComSerial
import time

sensor_dict = {
    "US": ("sensor ultra sonico", "cm", "US", "mide distancia"),
    "TE": ("sensor de temperatura", "°", "TE", "mide temperatura"),
    "HU": ("sensor humedad", "%", "HU", "mide humedad"),
    "FR": ("sensor fotoresistencia", "Lx", "FR", "mide la luz"),
    "RP": ("sensor de RPM", "rpm", "RP", "mide las revoluciones por minuto"),
    "IR": ("sensor de infrarojo", "estado", "IR", "revisa si hay obstaculos"),
    "IN": ("sensor de inclinacion", "estado", "IN", "revisa el estado del vehiculo"),
}

class ISG(Arreglo):
    
    def __init__(self, nombre=None, unidad=None, clave=None, descripcion=None, isf=ISF()):
        self.nombre = nombre
        self.unidad = unidad
        self.clave = clave
        self.descripcion = descripcion
        self.isf = isf if isf else []  
        super().__init__()  
        
    def __str__(self) -> str:
        return f"{self.nombre} ({self.unidad}) ({self.clave}) ({self.descripcion}) isf:({self.isf}) \nisf:\n{str(self.isf.get())}\n"
    
    def dictionary(self):
        return{
            "nombre": self.nombre,
            "unidad": self.unidad,
            "clave": self.clave,
            "descripcion": self.descripcion,
            "isf":[isf.dictionary() for isf in self.isf.arreglo]  
        }
        
    def ConvertoJson(self):
        c = [isg.dictionary() for isg in self.arreglo]
        with open("./isg.json", "w") as archivo:
            archivo.write(json.dumps(c, indent=4))

    def extract(self, json):
        extracted_isg = ""
        for isg_data in json:
            igg = ISG(isg_data['nombre'], isg_data['unidad'], isg_data['clave'], isg_data['descripcion'])
            igg.isf = ISF()  
            igg.isf.extract(isg_data['isf'])
            extracted_isg += str(igg) + "\n"
            self.post(igg)
        return extracted_isg.strip()
        
    def procesar_datos_com_serial(self):
     
        com_serial = ComSerial()

        datos = com_serial.datoSerial()

       
        for dato in datos:
            partes = dato.split('-')
            if len(partes) == 4:
                tipo_sensor, _, numeroSerie, data = partes
                
                if tipo_sensor in sensor_dict:
                    nombre, unidad, clave, descripcion = sensor_dict[tipo_sensor]
                   
                    d = Data(tipo_sensor, numeroSerie, data)
                    
                    igg = next((x for x in self.arreglo if x.clave == clave), None)
                    if igg:
                        
                        isf = next((x for x in igg.isf.arreglo if x.NoSerie == numeroSerie), None)
                        if isf:
                            
                            isf.data.post(d)
                        else:
                            
                            isf = ISF(numeroSerie, "COM1", Data())
                            isf.data.post(d)
                            igg.isf.arreglo = [isf]  
                    else:
                       
                        isf = ISF(numeroSerie, "COM1", Data())
                        isf.data.post(d)
                        igg = ISG(nombre, unidad, clave, descripcion, isf)
                        self.post(igg)

       
        self.ConvertoJson()

if __name__ == "__main__":
    x = ISG()
    
    while True:
        x.procesar_datos_com_serial()
        
        print(x.ConvertoJson())

        for c in x.arreglo: 
            print(c)
            print("isg:", type(c))
            print("isf:", type(c.isf))

            for s in c.isf.arreglo: 
                print("isf", type(s))
                
        time.sleep(5)
