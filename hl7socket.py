import select
import functions as fnc

from tcpsocket import TcpSocket

from datetime import datetime
from time import perf_counter


class ClientHL7(TcpSocket):

    def __init__(self, host, port, timeout: int = 2, code='utf-8'):
        super().__init__(host, port, code)
        self.timeout = timeout
        self.random = False
        self.accNumber = False

    def sendHL7(self):
        try:
            tSendEnd = 0.0
            tRecvEnd = 0.0
            if not self.run:
                return '', tSendEnd, tRecvEnd
            print('[CLIENT]: Message sending start')
            error = self.createClient(self.timeout)
            if error:
                return 'ERROR', tSendEnd, tRecvEnd
            t_start = perf_counter()
            self.outMsg = fnc.genSendingMessage(self.outMsg, self.code,
                                                self.random, self.accNumber,
                                                str(t_start))
            data = fnc.convertMessage(self.outMsg, self.code)
            self.write(self.sock, data)
            tSendEnd = perf_counter() - t_start
            print(f'[CLIENT]: Message sent for {tSendEnd}')
            data = self.read(self.sock, peek=True)
            tRecvEnd = perf_counter() - t_start - tSendEnd
            print(f'[CLIENT]: Answer received for {tRecvEnd}')
            self.inMsg = fnc.uconvertMessage(data, self.code)
            self.close(self.sock)
            return f"{datetime.now().strftime('%H:%M:%S')}", tSendEnd, tRecvEnd
        except Exception as exc:
            print(exc)


class ServerHL7(TcpSocket):

    def listen(self):
        print('[SERVER]: Start listen')
        inputs = [self.sock]
        #self.sock.getpeername()
        outputs = []
        while inputs:
            rlist, wlist, xlist = select.select(inputs, outputs, inputs)
            if not self.run:
                print('[SERVER]: Stopped listen')
                return '[STOPPED]', ''
            for sock in rlist:
                print('[SERVER]: Read!', sock)
                if sock is self.sock:
                    connection = self.accept()
                    if connection:
                        inputs.append(connection)
                else:
                    data = self.read(sock, 1)
                    self.inMsg = "No formating HL7 message received from client"
                    if data == b'\x0b':
                        self.inMsg = b''
                        data_all = b''
                        while data_all[-2:] != b'\x1c\r':
                            data = self.read(sock)
                            # print('[SERVER]: s.recv', data)
                            if not data:
                                break
                            data_all += data
                        self.inMsg = fnc.uconvertMessage(data_all, self.code)
                    inputs.remove(sock)
                    outputs.append(sock)

            for sock in wlist:
                sockpeer = sock.getpeername()
                print(f'[SERVER]: Write! {sock}')
                date = datetime.now()
                self.outMsg = fnc.genAnswerMessage(self.inMsg, self.code, date.strftime('%Y%m%d%H%M%S'))
                self.write(sock, fnc.convertMessage(self.outMsg, self.code))
                self.close(sock)
                outputs.remove(sock)
                return f"{date.strftime('%H:%M:%S')}", f'{sockpeer[0]}:{sockpeer[1]}'

            for sock in xlist:
                print('[SERVER]: Exception!!!')
                inputs.remove(sock)
                if sock in outputs:
                    outputs.remove(sock)
                self.close(sock)
                return '[ERROR]', ''
