#import hl7
from hl7 import parse

first_sim = b'\x0b'
cr_sim = b'\r'
last_sim = b'\x1c\r'


def transferToHL7(msg: str, code: str):
    msg = msg.strip().split('\n')
    result = ''
    for i in msg:
        result += i + cr_sim.decode(code)
    return result


def genAnswerMessage(msg: str, code: str, date: str) -> str:
    result = transferToHL7(msg, code)
    answer = ''
    try:
        result = parse(result)
        answer = f"MSH|^~\\&|{result['MSH'][0][5]}|{result['MSH'][0][6]}|{result['MSH'][0][3]}|{result['MSH'][0][4]}|{date}||ACK|||{result['MSH'][0][12]}\r"
        answer += f"MSA|AA|{result['MSH'][0][10]}|Сообщение успешно получено\r"
    except Exception as exc:
        print(exc)
    return answer


def genSendingMessage(msg: str,
                      code: str,
                      random: bool = False,
                      accNumber: bool = False,
                      timestamp: str = None) -> str:
    result = transferToHL7(msg, code)
    if random:
        try:
            result = parse(result)
            order = str(result['ORC'][0][1]).upper()
            if order == 'SC':
                result['MSH'][0][10] = timestamp
                result['ZDS'][0][1] = timestamp + '^'
                if accNumber:
                    start = str(result['ORC'][0][2])[:4]
                    end = int(str(result['ORC'][0][2])[4:]) + 1
                    result['ORC'][0][2] = f'{start}{end}'
            elif order == 'NW':
                result['MSH'][0][10] = timestamp
                result['ORC'][0][2] = timestamp
        except Exception as exc:
            result = exc
        finally:
            result = str(result)
    return result


def convertMessage(msg: str, code: str) -> bytes:
    result = first_sim + msg.encode(code) + last_sim
    return result


def uconvertMessage(msg: bytes, code: str) -> str:
    return msg.strip(first_sim + cr_sim + last_sim).decode(code)
