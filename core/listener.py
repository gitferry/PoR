import socket
import threading
import time
import random

PORT = 65535
THRESHOLD = 10
NUMBER = 1
NETWORKTYPE = '<broadcast>'

class BroadcastThread(threading.Thread):
    def __init__(self, type):
        threading.Thread.__init__(self)
        self.type = type

    def run(self):
        randomDelay = random.randint(1, 10)
        time.sleep(randomDelay)
        block = "block: Hello World"
        print "Broadcasting" + block
        broadcast(block)


def broadcast(message):
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_socket.sendto(message.encode('utf-8'), (NETWORKTYPE, PORT))
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

    receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    receive_socket.bind(('', PORT))
    print('Listening for broadcast at ', receive_socket.getsockname())

    while True:
        data, address = receive_socket.recvfrom(65535)
        print('Server received from {}:{}'.format(address, data.encode('utf-8')))
        if "transaction" in data:
            if transaction_count < threshold:
                transaction_count += 1
                print "transaction number: " + str(transaction_count)
            else:
                # randomNumber = random.randint(NUMBER)
                # if randomNumber == 1:
                blockThread = BroadcastThread('block')
                blockThread.run()
                transaction_count = 0
        elif "block" in data:
            print "block received"


def main():
    listenerThread = ListenerThread(THRESHOLD, NUMBER)
    listenerThread.run()

main()
