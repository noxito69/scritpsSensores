import serial, time

class ComSerial:
    def __init__(self, port = 'COM3', baudrate = 115200) -> None:
        self.port = port
        self.baudrate = baudrate

    def datoSerial(self, num_lineas=9):
        datos = []
        try:
            self.esp32 = serial.Serial(self.port, self.baudrate)
            time.sleep(2)

            while len(datos) < num_lineas:
                if self.esp32.in_waiting > 0:
                    datoSerial = self.esp32.readline().decode().strip()
                    if not datoSerial.startswith("E ("):
                        print(datoSerial)
                        datos.append(datoSerial)

            self.esp32.close()

        except serial.SerialException:
            print("\nNo se puede abrir el puerto serial porque hay otra gata rompehogares usando el puerto, cierralo >:c\n")

        return datos
    
if __name__ == "__main__":
    # esto ya es para que muestre los datos que me manda el serial loco, simplemente waos 
    x = ComSerial()
    x.datoSerial()
