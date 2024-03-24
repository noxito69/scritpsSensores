from sala import Sala
from sala import Funcion
from arreglo import Arreglo
import json

class Cine(Arreglo):
    
    def __init__(self, nombre=None, direccion=None, estado=None, tipoCine=None, numeroSalas=None, sala=Sala()):
        self.nombre = nombre
        self.direccion = direccion
        self.estado = estado
        self.tipoCine = tipoCine
        self.numeroSalas = numeroSalas
        self.sala = sala if sala else []
        super().__init__()
        

        
        
    def __str__(self) -> str:
        return f"{self.nombre} ({self.direccion}) ({self.estado}) ({self.tipoCine}) ({self.numeroSalas}) Salas:({self.sala}) \nSalas:\n{str(self.sala.get())}\n"
    
    def dictionary(self):
        return{
            "nombre": self.nombre,
            "direccion": self.direccion,
            "estado": self.estado,
            "tipoCine": self.tipoCine,
            "numeroSalas": self.numeroSalas,
            "salas": [sala.dictionary() for sala in self.sala.arreglo]  # Ajusta aquí
        }
        
    def ConvertoJson(self):
        cines = [cine.dictionary() for cine in self.arreglo]
        with open("./cines.json", "w") as archivo:
            archivo.write(json.dumps(cines, indent=4))

            
        
    def extract(self, json):
        cine_str = ""
        sala = Sala()
        for cine in json:
            cin = Cine(cine['nombre'], cine['direccion'], cine['estado'], cine['tipoCine'], cine['numeroSalas'], Sala())
            cin.sala.extract(cine['salas'])
            cine_str += str(cin) + "\n"
            self.post(cin)

        return cine_str.strip()
        
        
if __name__ == "__main__":
    
    x = Cine()
    S = Sala()
    
    print(x.extract(x.extraer_json("cines")))
    
    
    for c in x.arreglo: 
        print(c)
        print("Cine:",type(c))
        print("Sala:", type(c.sala))
        #print("Funcion:", type(c.sala.arreglo[0].funcion))

        for s in c.sala.arreglo: 
            print("Sala",type(s))
            
        
            for f in s.funcion.arreglo: 
                print("Funcion",type(f))    


    """c
        
    
    funcion = Funcion("Interestellar", "6:30 PM",1,80, 169, "Ciencia ficción")
    funcion1 = Funcion("300", "6:30 PM",1,80, 169, "drama")
    S = Sala(1, 100, "Proyector WPX 4500", "3X500 SONY", "VIP",Funcion())
    S1 = Sala(1, 100, "Proyector WPX 4500", "3X500 SONY", "VIP",Funcion())
    
    C = Cine("Cinemex Torreon", "Calle 5 de Mayo #123","Abierto","Cinemex", 10)
    
    S.funcion.post(funcion)
    C.sala.append(S)
    S.funcion.post(funcion1)
    C.sala.append(S1)


    x.post(C)

    print(x.ConvertoJson())
   

    """
