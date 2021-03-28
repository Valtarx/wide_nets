from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

authorizer = DummyAuthorizer()
authorizer.add_user("user", "12345", "C:/Users/Кова/Desktop/ftp", perm="elradfmw",
                    msg_login="Добро пожаловать на FTP-сервер!", msg_quit="До новых встреч!")
authorizer.add_anonymous("C:/Users/Кова/Desktop/ftp", perm="elr",
                         msg_login="Вы вошли на сервер в качестве гостя, поэтому имеете право "
                                   "только на чтение и скачивание.",
                         msg_quit="До новых встреч!")

handler = FTPHandler
handler.authorizer = authorizer

text = "Выберите режим работы сервера: \n" \
       "1 - Активный режим \n" \
       "2 - Пассивный режим \n"

while True:
    mode = input(text)
    if mode == "1" or mode == "2":
        break
    else:
        print("Ожидался ввод одного из чисел.")

if mode == "1":
    server = FTPServer(("127.0.0.1", 1026), handler)
    server.serve_forever()
elif mode == "2":
    handler.passive_ports = range(60000, 65535)
    server = FTPServer(("127.0.0.1", 1026), handler)
    server.serve_forever()
