#python -m consumer test_topic
#https://andres-plazas.medium.com/leer-y-escribir-datos-en-kafka-usando-python-2696154c3948

from kafka import KafkaConsumer
import json
import numpy as np


class Consumer:
    def __init__(self, topic):
        #self._consumer = KafkaConsumer(topic, bootstrap_servers='localhost:9092', value_deserializer=lambda x: x.decode('utf-8'), group_id='tfm')
        self._consumer = KafkaConsumer(topic, bootstrap_servers='localhost:9092', value_deserializer=lambda x: json.loads(x.decode('utf-8')), group_id='tfm')

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
            message_count += 1


if __name__ == '__main__':
    pass