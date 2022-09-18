#python -m consumer test_topic
#https://andres-plazas.medium.com/leer-y-escribir-datos-en-kafka-usando-python-2696154c3948

from kafka import KafkaConsumer
from tensorflow.keras.models import  model_from_json
import json
import numpy as np
import cv2
from datetime import datetime


class Consumer:
    def __init__(self, topic):
        self._consumer = KafkaConsumer(topic, bootstrap_servers='172.20.10.7:9092', value_deserializer=lambda x: json.loads(x.decode('utf-8')), group_id='tfm')

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

        #Load trained model
        json_file = open('C:/Users/pablo/Documents/Master Big Data/0-Trabajo de Fin de Master/Repositorio Git/TFM-Big-Data/models/model_structure.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("C:/Users/pablo/Documents/Master Big Data/0-Trabajo de Fin de Master/Repositorio Git/TFM-Big-Data/models/model_weights.h5")

        for message in self._consumer:
            message = message.value
            print(f'Message {message_count}: {np.array(message["image"]).shape}')
            print(f'Message {message_count}: {np.array(message["image"])[0].shape}')

            b,g,r = cv2.split(np.array(message["image"])[0])
            img = cv2.merge([r,g,b])

            prediction = loaded_model.predict(np.array([img]))
            print(prediction)
            now = datetime.now()

            #Save results in log
            with open('C:/Users/pablo/Documents/Master Big Data/0-Trabajo de Fin de Master/Repositorio Git/TFM-Big-Data/reports/predictions/Log.log', 'a') as f:
                f.write('\n' + now.strftime("%Y/%m/%d %H:%M:%S_%f") + ' - Screenshot prediction: '+str(prediction))
            
            if(prediction[0][0]>0.5):
                folder = 'C:/Users/pablo/Documents/Master Big Data/0-Trabajo de Fin de Master/Repositorio Git/TFM-Big-Data/reports/predictions/No-Chating/'
            else:
                folder = 'C:/Users/pablo/Documents/Master Big Data/0-Trabajo de Fin de Master/Repositorio Git/TFM-Big-Data/reports/predictions/WhatsApp/'

            cv2.imwrite(folder + now.strftime("%Y%m%d_%H%M%S_%f")+".png",img)
            message_count += 1


if __name__ == '__main__':
    pass