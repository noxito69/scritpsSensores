from arreglo import Arreglo
from data import Data
import json

class Sala(Arreglo):
    
    def __init__(self, numero_sala=None, capacidad=None, proyector=None, audio=None, tipo=None, funcion=Funcion()):
        self.numero_sala = numero_sala
        self.capacidad = capacidad
        self.proyector = proyector
        self.audio = audio
        self.tipo = tipo
        self.funcion = funcion if funcion else []
        super().__init__()
    
    def __str__(self) -> str:
        return f"Sala {self.numero_sala} ({self.capacidad} asientos) ({self.proyector}) ({self.audio}) ({self.tipo}) {self.funcion} \nFunciones:\n {str(self.funcion.get())}\n"
        
    def dictionary(self):
        return{
            "numero_sala":self.numero_sala,
            "capacidad":self.capacidad,
            "proyector":self.proyector,
            "audio":self.audio,
            "tipo":self.tipo,
            "funcion":[funcion.dictionary() for funcion in self.funcion.arreglo]
        }
        
    def ConvertoJson(self):
        salas = [sala.dictionary() for sala in self.arreglo]
        with open("./salas.json", "w") as archivo:
            archivo.write(json.dumps(salas, indent=4))
            
    def extract(self, json):
        salas_str = ""
        for sala in json:
            sa = Sala(sala['numero_sala'], sala['capacidad'], sala['proyector'], sala['audio'], sala['tipo'], Funcion())
            sa.funcion.extract_funciones(sala['funcion'])
            salas_str += str(sa) + "\n"
            self.post(sa)
        return salas_str.strip()




        
    
if __name__ == "__main__":
    
    x = Sala()
    
    x.extract(x.extraer_json("salas"))

    for sala in x.arreglo:
        print("Sala",type(sala))
        print("Sala",type(sala.funcion))
        for f in sala.funcion.arreglo: 
            print("Funcion",type(f))
            
    funcion = Funcion("Interestellar", "6:30 PM",1,80, 169, "Ciencia ficcion")
    funcion2 = Funcion("TOY STORY", "8:30 PM",1,80, 169, "infantil")
    S = Sala(1, 100, "Proyector WPX 4500", "3X500 SONY", "VIP", Funcion())
   
    
    S.funcion.post(funcion)
    S.funcion.post(funcion2)
    
    x.post(S)
    
    
    print(x.ConvertoJson())


