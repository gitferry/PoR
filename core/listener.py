import sys
import socket
import threading
import time
import random
import os

PORT = 65535
THRESHOLD = 10
NUMBER = 1
NETWORKTYPE = '<broadcast>'
TRANSACTION_SIZE = 10

class BroadcastThread(threading.Thread):
    def __init__(self, type, threshold):
        threading.Thread.__init__(self)
        self.type = type
        self.threshold = threshold

    def run(self):
        randomDelay = random.randint(1, 10)
        time.sleep(randomDelay)
        block = "block: Hello World"
        print "Broadcasting" + block
        broadcast(block, self.threshold)


def broadcast(message, threshold):
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_socket.sendto(message + os.urandom(8+threshold*TRANSACTION_SIZE), (NETWORKTYPE, PORT))
    print message + "sent"

class ListenerThread(threading.Thread):
    def __init__(self, threshold, number):
        threading.Thread.__init__(self)
        self.threshold = threshold
        self.number = number

    def run(self):
        receive(self.threshold, self.number)

def receive(threshold, number):
    transaction_count = 0
    blcok_count = 0

    receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    receive_socket.bind(('', PORT))
    print('Listening for broadcast at ', receive_socket.getsockname())

    while True:
        data, address = receive_socket.recvfrom(1999999)
        print('Server received from {}'.format(address))
        if "transaction" in data:
            if transaction_count < threshold:
                transaction_count += 1
                print "transaction number: " + str(transaction_count)
            else:
                randomNumber = random.randint(1, number)
                transaction_count = 0
                if randomNumber == 1:
                    blockThread = BroadcastThread('block', threshold)
                    blockThread.run()
        elif "block" in data:
            blcok_count += 1
            print "block received, blcok_number: " + str(blcok_count)


def main():
    if sys.argv[1]:
        threshold = int(sys.argv[1])
    else:
        threshold = THRESHOLD
    if sys.argv[2]:
        number = int(sys.argv[2])
    else:
        number = NUMBER
    listenerThread = ListenerThread(threshold, number)
    listenerThread.run()

if __name__ == '__main__':
    main()
