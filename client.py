import socket
import pickle
import random

import hamming as h

WORD_LENGTH = 57

ERRORS_PER_WORD = int(input('Errors number: '))


def makeErrors(data, number=1):
    positions = random.sample(range(len(data) - 1), number)

    for position in positions:
        if data[position] == '0':
            data = h.changeChar(data, position, '1')
        else:
            data = h.changeChar(data, position, '0')

    return data


data = ''
with open('message.txt', 'r') as file:
    data = file.read()

data = data.encode('utf8')
data = ''.join(item[2:] for item in map(bin, data))
data = h.splitData(data, WORD_LENGTH)
controlBitsNumber = h.controlBitsNumber(WORD_LENGTH)

for i in range(len(data)):
    data[i] = h.encode(data[i], controlBitsNumber)

if ERRORS_PER_WORD != 0:
    sample = random.sample(range(len(data)), int(len(data) / 2))
    for word in sample:
        data[word] = makeErrors(data[word], ERRORS_PER_WORD)

sock = socket.socket()
sock.connect(('localhost', 9090))
sock.sendall(pickle.dumps(data))
sock.close()

sock = socket.socket()
sock.bind(('', 9091))
sock.listen(1)
conn, addr = sock.accept()

message = ""

while True:
    packet = conn.recv(4096)
    if not packet:
        break
    message += packet.decode()

print(message)

sock.close()

input('')
