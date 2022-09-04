from .producer import Producer
import sys


if __name__ == '__main__':
    producer = Producer(sys.argv[1], sys.argv[2])
    producer.start_write()