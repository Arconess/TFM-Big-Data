#python -m consumer test_topic
#https://andres-plazas.medium.com/leer-y-escribir-datos-en-kafka-usando-python-2696154c3948

from kafka import KafkaConsumer
import json
import numpy as np
import cv2


class Consumer:
    def __init__(self, topic):
        self._consumer = KafkaConsumer(topic, bootstrap_servers='192.168.1.147:9092', value_deserializer=lambda x: json.loads(x.decode('utf-8')), group_id='tfm')

    @property
    def consumer(self):
        return self._consumer

    @consumer.setter
    def consumer(self, value):
        if isinstance(value, KafkaConsumer):
            self._consumer = value

    def star_read(self):
        self.receive_message()

    def receive_message(self):
        message_count = 0
        for message in self._consumer:
            message = message.value
            print(f'Message {message_count}: {np.array(message["image"]).shape}')
            print(f'Message {message_count}: {np.array(message["image"])[0].shape}')

            b,g,r = cv2.split(np.array(message["image"])[0])
            img = cv2.merge([r,g,b])

            
            cv2.imwrite("./test.png",img)
            message_count += 1


if __name__ == '__main__':
    pass