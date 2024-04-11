from isf import ISF
from data import Data
from arreglo import Arreglo
import json
 
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
        
        
if __name__ == "__main__":
    
    x = ISG()
    S = ISF()
    
    print(x.extract(x.extraer_json("isg")))
    
    
    for c in x.arreglo: 
        print(c)
        print("isg:",type(c))
        print("isf:", type(c.isf))
        #print("Funcion:", type(c.sala.arreglo[0].funcion))

        for s in c.isf.arreglo: 
            print("isf",type(s))
            
        
            for f in s.data.arreglo: 
                print("data",type(f))    


    
        
    
    data = Data("US", 1, "1195")
    S = ISF("123","COM1",Data())
    
    C = ISG("sensor ultra sonico","cm","US","mide distancia",ISF())
    
    S.data.post(data)
    C.isf.arreglo.append(S)
   
    

    x.post(C)

    print(x.ConvertoJson())
   

    
