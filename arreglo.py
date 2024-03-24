import json
class Arreglo:
    
    
    def __init__(self):
        self.arreglo=[]
        
    def post(self, item):
        self.arreglo.append(item)
        
    def get(self):
        return "\n".join([str(item)for item in self.arreglo])
    
        
    def update(self, newItem, item):
        if self.arreglo == []:
            return "No hay elementos en el arreglo"
        
        else:
            self.arreglo.remove(item)
            self.arreglo.append(newItem)
            return "se modifico {item}"
    
    def delete(self,item):
        if self.arreglo ==[]:
            return "no se encontro el item"
        else:
            self.arreglo.remove(item)
            return " se elimino {item}"
        
        
    def extraer_json(self, nombre):
        with open(f'./{nombre}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data