import json
import sys 
import threading
from confluent_kafka import Consumer
from confluent_kafka import KafkaError
from confluent_kafka import KafkaException


running=True
conf = {'bootstrap.servers': "localhost:9092",
        'auto.offset.reset': 'smallest',
        'group.id': "user_group"}
topic='topic_user_created'


class UserCreatedListener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.consumer = Consumer(conf)
   
        
    def run(self):
        print ('Inside Logging :  Created Listener ')
        try:
            self.consumer.subscribe([topic])

            while running:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None: continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                        sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
                else:
                    print('----------Got message-----------')
                    message = json.loads(msg.value().decode('utf-8'))
                    print(message)
        finally:
        # Close down consumer to commit final offsets.
            self.consumer.close()
    
   