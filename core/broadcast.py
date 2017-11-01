import socket

PORT = 1060
NETWORKTYPE = '<broadcast>'

broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcast_socket.sendto('Client broadcast message!'.encode('utf-8'), (NETWORKTYPE, PORT))

receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

receive_socket.bind(('127.0.0.1', PORT))
print('Listening for broadcast at ', receive_socket.getsockname())

while True:
    data, address = receive_socket.recvfrom(65535)
    print('Server received from {}:{}'.format(address, data.decode('utf-8')))
