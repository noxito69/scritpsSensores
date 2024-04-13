from isf import ISF
from data import Data
from arreglo import Arreglo
import json
from comSerial import ComSerial
 
class ISG(Arreglo):
    
    def __init__(self, nombre=None, unidad=None, clave=None, descripcion=None, numeroSalas=None, isf=ISF()):
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
        isf = ISF()
        for isg_data in json:
            igg = ISG(isg_data['nombre'], isg_data['unidad'], isg_data['clave'], isg_data['descripcion'], ISF())
            igg.isf.extract(isg_data['isf'])
            extracted_isg += str(igg) + "\n"
            self.post(igg)

        return extracted_isg.strip()
        
    def procesar_datos_com_serial(self):
        # Crear una instancia de ComSerial
        com_serial = ComSerial()

        # Obtener los datos de ComSerial
        datos = com_serial.datoSerial()

        # guarda las instancias
        data_instances = []

        # Procesar los datos
        for dato in datos:
            partes = dato.split('-')
            if len(partes) == 4:
                tipo_sensor, _, numeroSerie, data = partes
                # Crear una instancia de Data
                d = Data(tipo_sensor, numeroSerie, data)

                data_instances.append(d)

        return data_instances

                # Crear una instancia de ISF y agregar la instancia de Data
                #s = ISF("123", "COM6", d)
                # Agregar la instancia de ISF a ISG
                #self.isf.arreglo.append(s)

        # Guardar los datos en un archivo JSON
        #self.ConvertoJson()
        
if __name__ == "__main__":
    x = ISG()
    data_instances = x.procesar_datos_com_serial()
    
    for data in data_instances:
        S = ISF()
        #data = data_instances[i]
        S = ISF("123","COM6",data)
        C = ISG("sensor ultra sonico","cm","US","mide distancia",ISF())
        S.data.post(data)
        C.isf.arreglo.append(S)
        x.post(C)

    print(x.ConvertoJson())

    for c in x.arreglo: 
        print(c)
        print("isg:",type(c))
        print("isf:", type(c.isf))

        for s in c.isf.arreglo: 
            print("isf",type(s))

# CREAR UNA CLASE QUE PUEDA MAPEAR LOS DATOS DE ISG.JSON Y QUE LOS ACOMODE SEGÚN UN FORMATO MAS LEGIBLE PARA QUE LA CONSULTA DE GET NOMAS SEA 1 Y NO ANDAR PIDIENDO TANTAS VECES LOS DATOS 