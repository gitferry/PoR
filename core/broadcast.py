import socket
import threading
import time
import random
import os

PORT = 65535
THRESHOLD = 10
NUMBER = 1
NETWORKTYPE = '<broadcast>'
TRANSACTION_SIZE = 100

class BroadcastThread(threading.Thread):
    def __init__(self, type):
        threading.Thread.__init__(self)
        self.type = type

    def run(self):
        transaction = "transaction: Hello World"
        print "Broadcasting" + transaction
        broadcast(transaction)

def broadcast(message):
    while True:
        randomDelay = random.randint(1, 10)
        time.sleep(randomDelay)
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        broadcast_socket.sendto(message+os.urandom(100), (NETWORKTYPE, PORT))
        print message + "sent"

def main():
    transactionThread = BroadcastThread(type="transaction")
    transactionThread.run()


main()
