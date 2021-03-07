import socket
import pickle
import hamming as h

WORD_LENGTH = 57
controlBitsNumber = h.controlBitsNumber(WORD_LENGTH)

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()

data = []
while True:
    packet = conn.recv(4096)
    if not packet:
        print("Get all data")
        break
    data.append(packet)

data = pickle.loads(b"".join(data))

multipleErrors = []
errorsNumber = 0

for i in range(len(data)):
    position = h.detectErrors(data[i], controlBitsNumber)
    if position is not None:
        errorsNumber += 1
        if position != -1:
            data[i] = h.correctError(data[i], position)
        else:
            multipleErrors.append(i)


for i in range(len(data)):
    if i not in multipleErrors:
        data[i] = h.decode(data[i], controlBitsNumber)

message = "Received: {0} \n" \
          "With no errors: {1}\n" \
          "With errors: {2}\n" \
          "Fixed: {3}".format(
    len(data), len(data) - errorsNumber, errorsNumber, errorsNumber - len(multipleErrors))

print(message)

sock = socket.socket()
sock.connect(('localhost', 9091))
sock.sendall(message.encode())
sock.close()

input('')
