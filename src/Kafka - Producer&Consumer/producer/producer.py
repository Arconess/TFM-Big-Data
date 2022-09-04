#python -m producer test_topic 5
#https://andres-plazas.medium.com/leer-y-escribir-datos-en-kafka-usando-python-2696154c3948

from kafka import KafkaProducer
import time
import pyautogui
import numpy as np
import json
import cv2

class Producer:
    def __init__(self, topic, freq):
        self.topic = topic
        self.freq = freq if isinstance(freq, int) else int(freq)
        #self.producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda x: x.encode('utf-8'))
        self.producer = KafkaProducer(bootstrap_servers='192.168.1.147:9092', value_serializer=lambda x: json.dumps(x).encode('utf-8'))

    def start_write(self):
        for value in ['1']:
            img = pyautogui.screenshot(region=(0,0,20,30)) #region=(0,0,20,30)
            img = np.array(img)
            cv2.resize(img, (5,2), interpolation=cv2.INTER_CUBIC)#198,96

            d = {"image": [np.asarray(img).tolist()]}#[np.asarray(img).tolist()]}
            #msg = dict(pd.DataFrame(data=d).iloc[0])

            #self.producer.send(self.topic, value={"image": "msg test", "test": "testing"})
            self.producer.send(self.topic, value=d)

            print("Enviados")
            time.sleep(self.freq)


if __name__ == '__main__':
    pass