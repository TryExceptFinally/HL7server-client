import socket


class TcpSocket:

    def __init__(self, host: str, port: int, code: str = 'utf-8'):
        self.host = host
        self.port = port
        self.outMsg = ''
        self.inMsg = ''
        self.code = code
        self.sock = None
        self.run = False

    def exception(self, name: str, exc):
        print(f'[{name}]: {exc}')
        self.close(self.sock)
        self.run = False

    def createClient(self, timeout: int) -> str:
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(timeout)
            self.sock.connect((self.host, self.port))
            return ''
        except OSError as exc:
            self.exception('CreateCLIENT', exc)
            return f'{exc}'

    def createServer(self):
        try:
            self.sock = socket.create_server(('', self.port),
                                             family=socket.AF_INET)
        except OSError as exc:
            self.exception('CreateSERVER', exc)

    def accept(self):
        try:
            connection, client_address = self.sock.accept()
            connection.setblocking(False)
            print(f'[SERVER]: {client_address} - connected')
            return connection
        except OSError as exc:
            self.exception('AcceptSERVER', exc)
            return ''

    def read(self, sock, rbytes: int = 1024, peek: bool = False) -> bytes:
        try:
            if peek:
                data = sock.recv(rbytes, socket.MSG_PEEK)
            else:
                data = sock.recv(rbytes)
            return data
        # except OSError as exc:
        #     print(f'[READ {sock}]: {exc}')
        #     return b''
        except (ConnectionResetError, ConnectionAbortedError,
                AttributeError, OSError) as exc:
            print(f'[READ {sock}]: {exc}')
            self.close(sock)
            return b''

    def write(self, sock, data: bytes):
        try:
            sock.send(data)
        except OSError as exc:
            print(f'[WRITE {sock}]: {exc}')
            self.close(sock)

    @staticmethod
    def close(sock):
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except:
            pass
        try:
            sock.close()
        except:
            pass
