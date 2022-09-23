import os.path
import sys
import signal

from sysargs import SysArgs
from hl7socket import ClientHL7


class Spamer():

    def __init__(self, fp, spam):
        self.fp = fp
        self.spam = spam

    def loadMsg(self):
        try:
            with open(self.fp, encoding=client.code, mode='r') as f:
                data = f.read()
                return data
        except Exception as exp:
            print(exp)

    def start(self):
        client.run = True
        client.outMsg = self.loadMsg()
        tAllRecv = 0.0
        countMsg = 0
        maxRecv = 0.0
        minRecv = client.timeout
        while (countMsg < self.spam) and client.run:
            countMsg += 1
            timeMsg, tSendEnd, tRecvEnd = client.sendHL7()
            tAllRecv += tRecvEnd
            if maxRecv < tRecvEnd:
                maxRecv = tRecvEnd
            if minRecv > tRecvEnd:
                minRecv = tRecvEnd
            print(
                f'[{timeMsg}] Message №{countMsg}, Sending: {tSendEnd:.5f}, Receiving: {tRecvEnd:.5f}'
            )
            print('-' * 60)
            print(client.inMsg.replace('\r', '\n'))
            print('-' * 60)
        print(
            f'Time receiving {countMsg} messages - Min: {minRecv:.5f}, Average: {tAllRecv/countMsg:.5f}, Max: {maxRecv:.5f}'
        )
        client.run = False


def sigint_handler(signal, frame):
    # print('Start stopping service...')
    client.run = False


if __name__ == '__main__':
    args = SysArgs()
    args = args.parser.parse_args()
    if not os.path.exists(args.filepath):
        print('filepath - error')
        sys.exit()
    client = ClientHL7(args.ip, args.port, args.timeout)
    client.accNumber = args.accnumber
    client.random = args.random
    spamer = Spamer(args.filepath, args.spam)
    args = None
    signal.signal(signal.SIGINT, sigint_handler)
    spamer.start()
