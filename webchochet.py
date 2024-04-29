import json
import threading
from websocket import WebSocketApp, enableTrace
import serial


ser = serial.Serial('/dev/ttyUSB0', 115200) 

def on_message(ws, message):
    print(f"Received message: {message}")
    print_value(message)

def on_error(ws, error):
    print(f"Encountered error: {error}")

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run():
        subscribe_message = {
            "event": "pusher:subscribe",
            "data": {
                "channel": "valores"
            }
        }
        ws.send(json.dumps(subscribe_message))

    thread = threading.Thread(target=run)
    thread.start()

def print_value(message):
   
    message_json = json.loads(message)

   
    data_json = json.loads(message_json["data"])


    value = data_json["valor"]["value"]

  
    print(value)
    ser.write(value.encode())  

if __name__ == "__main__":
    enableTrace(False)
    ws = WebSocketApp(
        "wss://ws-us2.pusher.com/app/626e6ebc0cf2b7caf83c?protocol=7&client=js&version=7.0.0&flash=false",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()