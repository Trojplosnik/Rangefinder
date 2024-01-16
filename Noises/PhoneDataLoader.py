import websocket
import json


def on_message(ws, message):
    values = json.loads(message)['values']
    x = values[0]
    y = values[1]
    z = values[2]
    print("x = ", x, "y = ", y, "z = ", z)


def on_error(ws, error):
    print("### error ###")
    print(error)


def on_close(ws, close_code, reason):
    print("### closed ###")
    print("close code : ", close_code)
    print("reason : ", reason)


def on_open(ws):
    print("connection opened")


if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://192.168.1.119:8080/sensor/connect?type=android.sensor.accelerometer",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()
