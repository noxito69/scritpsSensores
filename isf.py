from arreglo import Arreglo
from data import Data
import json

class ISF(Arreglo):
    
    def __init__(self, NoSerie=None, puerto=None, proyector=None, audio=None, tipo=None, data=Data()):
        self.NoSerie = NoSerie
        self.puerto = puerto
        self.data = data if data else []
        super().__init__()
    
    def __str__(self) -> str:
        return f"No.Serie: {self.NoSerie} (Puerto:{self.puerto} ) {self.data} \ndata:\n {str(self.data.get())}\n"
                
    def dictionary(self):
        return{
            "NoSerie":self.NoSerie,
            "puerto":self.puerto,
            "Data":[data.dictionary() for data in self.data.arreglo]
        }
        
    def ConvertoJson(self):
        datas = [isf.dictionary() for isf in self.arreglo]
        with open("./isf.json", "w") as archivo:
            archivo.write(json.dumps(datas, indent=4))
            
    def extract(self, json):
        isf_str = ""
        for isf_dict in json:
            sa = ISF(isf_dict['NoSerie'], isf_dict['puerto'], Data())
            sa.data.extract_data(isf_dict['Data'])
            isf_str += str(sa) + "\n"
            self.post(sa)
        return isf_str.strip()
        




        
    
if __name__ == "__main__":
    
    x = ISF()
    
    print(x.extract(x.extraer_json("ISF")))

    for isf in x.arreglo:
        print("isf",type(isf))
        print("isf",type(isf.data))
        for f in isf.data.arreglo: 
            print("data",type(f))
            
    data = Data("US", 1, "1195")
    isf = ISF("123","COM1",Data())
  
   
    
    isf.data.post(data)

    
    x.post(isf)
    
    
    print(x.ConvertoJson())


