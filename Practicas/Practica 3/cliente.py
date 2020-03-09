import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 12333)
print('Levantando servidor {} en el puerto {}'.format(*server_address))
sock.connect(server_address)

try:

    # Send data
    message = b'Este es el mensaje del cliente.'
    print('Información a enviar {!r}'.format(message))
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(1024)
        amount_received += len(data)
        print('Recibido del servidor: {!r}'.format(data))

finally:
    print('Cerrando canal de comunicación del cliente')
    sock.close()