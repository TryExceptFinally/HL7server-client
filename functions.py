# import hl7
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


def genAnswerMessage(msg: str, code: str, date: str, ack: str) -> str:
    result = transferToHL7(msg, code)
    answer = ''
    try:
        result = parse(result)
        answer = f"MSH|^~\\&|{result['MSH'][0][5]}|{result['MSH'][0][6]}|{result['MSH'][0][3]}|{result['MSH'][0][4]}|{date}||ACK|||{result['MSH'][0][12]}\r"
        answer += f"MSA|{ack}|{result['MSH'][0][10]}|Сообщение успешно получено\r"
    except Exception as exc:
        answer += f'[ERROR]: {exc}'
    finally:
        return answer


def genSendingMessage(msg: str,
                      code: str,
                      time_stamp: str = None,
                      acc_number: bool = False,
                      cur_time: str = None) -> str:
    result = transferToHL7(msg, code)
    if time_stamp or cur_time:
        try:
            result = parse(result)
            order = str(result['ORC'][0][1]).upper()
            if order == 'SC':
                if time_stamp:
                    result['MSH'][0][10] = time_stamp
                    result['ZDS'][0][1] = time_stamp + '^'
                    if acc_number:
                        start = str(result['ORC'][0][2])[:4]
                        end = int(str(result['ORC'][0][2])[4:]) + 1
                        result['ORC'][0][2] = f'{start}{end}'
                if cur_time:
                    result['MSH'][0][7] = cur_time
                    result['ZDS'][0][3] = cur_time
            elif order == 'NW':
                if time_stamp:
                    result['MSH'][0][10] = time_stamp
                    result['ORC'][0][2] = time_stamp
                if cur_time:
                    result['MSH'][0][7] = cur_time
                    result['OBR'][0][27] = cur_time
        except Exception as exc:
            result = exc
        finally:
            result = str(result)
    return result


def convertMessage(msg: str, code: str) -> bytes:
    result = first_sim + msg.encode(code) + last_sim
    return result


def uconvertMessage(msg: bytes, code: str) -> str:
    try:
        return msg.strip(first_sim + cr_sim + last_sim).decode(code)
    except UnicodeDecodeError:
        return 'UnicodeDecodeError'
