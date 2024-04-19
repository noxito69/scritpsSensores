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
        
        self.isf = isf if isf else []  # Crear una nueva instancia de ISF si no se proporciona ninguna
        super().__init__()  
        
    def __str__(self) -> str:
        return f"{self.nombre} ({self.unidad}) ({self.clave}) ({self.descripcion}) isf:({self.isf}) \nisf:\n{str(self.isf.get())}\n"
    
    def dictionary(self):
        isf_dict = {}  # Creamos un diccionario vacío para almacenar la información de ISF
        if self.isf.arreglo:  # Verificamos si hay instancias de ISF en el arreglo
            isf_dict = self.isf.arreglo[0].dictionary()  # Tomamos solo el primer elemento del arreglo de ISF
        return {
            "nombre": self.nombre,
            "unidad": self.unidad,
            "clave": self.clave,
            "descripcion": self.descripcion,
            "isf": isf_dict
        }
        
    def ConvertoJson(self):
        isg_dicts = [isg.dictionary() for isg in self.arreglo]
        with open("./isg.json", "w") as archivo:
            archivo.write(json.dumps(isg_dicts, indent=4))

    def extract(self, json):
        extracted_isg = ""
        for isg_data in json:
            igg = ISG(isg_data['nombre'], isg_data['unidad'], isg_data['clave'], isg_data['descripcion'])
            igg.isf = ISF()  # Crear una nueva instancia de ISF
            igg.isf.extract(isg_data['isf'])
            extracted_isg += str(igg) + "\n"
            self.post(igg)
        return extracted_isg.strip()
        
    def procesar_datos_com_serial(self):
        # Crear una instancia de ComSerial
        com_serial = ComSerial()

        # Obtener los datos de ComSerial
        datos = com_serial.datoSerial()

        # Procesar los datos
        for dato in datos:
            partes = dato.split('-')
            if len(partes) == 4:
                tipo_sensor, _, numeroSerie, data = partes
                # Verificar si el tipo de sensor está en el diccionario
                if tipo_sensor in sensor_dict:
                    nombre, unidad, clave, descripcion = sensor_dict[tipo_sensor]
                    # Verificar si ya existe una instancia de ISF con el mismo número de serie
                    isf_existente = next((isf for isf in self.isf.arreglo if isf.NoSerie == numeroSerie), None)
                    if isf_existente:
                        # Si existe, usar la instancia existente de ISF
                        isf = isf_existente
                    else:
                        # Si no existe, crear una nueva instancia de ISF con los datos del sensor
                        isf = ISF("1", "COM1", Data())
                        self.isf.arreglo.append(isf)
                    
                    # Crear una instancia de Data con los datos del sensor
                    d = Data(tipo_sensor, numeroSerie, data)
                    # Agregar la instancia de Data a ISF
                    isf.data.post(d)

                    # Crear una instancia de ISG si aún no existe
                    if not self.arreglo:
                        igg = ISG(nombre, unidad, clave, descripcion, isf)
                        self.post(igg)
                    else:
                        # Buscar si ya existe una instancia de ISG con el mismo tipo de sensor
                        igg = next((x for x in self.arreglo if x.clave == clave), None)
                        if igg:
                            # Si ya existe, agregar ISF a esa instancia de ISG
                            igg.isf.arreglo.append(isf)
                        else:
                            # Si no existe, crear una nueva instancia de ISG y agregar ISF
                            igg = ISG(nombre, unidad, clave, descripcion, isf)
                            self.post(igg)

        # Guardar los datos en un archivo JSON
        self.ConvertoJson()

if __name__ == "__main__":
    x = ISG()
    
    while True:
        x.procesar_datos_com_serial()
        
        print(x.ConvertoJson())
                
        time.sleep(1.5)