import argparse


class SysArgs():

    def __init__(self):
        DEFAULT_PORT = 6005
        DEFAULT_TIMEOUT = 3
        DEFAULT_SPAM = 1
        DEFAULT_RANDOM = False
        DEFAULT_AN = False
        DEFAULT_CUR_TIME = False
        self.parser = argparse.ArgumentParser(
            description='Running a HL7 test from the command line')
        try:
            self.parser.add_argument(
                '-fp', '--filepath', type=str, help='Path to HL7 file', metavar='', required=True)
            self.parser.add_argument(
                '-i', '--ip', type=str, help='IP address or domain name to connect', metavar='', required=True)
            self.parser.add_argument(
                '-p', '--port', type=int, help=f'Port to connect (default: {DEFAULT_PORT})', metavar='',
                default=DEFAULT_PORT)
            self.parser.add_argument(
                '-t', '--timeout', type=int, help=f'Connection time-out (default: {DEFAULT_TIMEOUT})', metavar='',
                default=DEFAULT_TIMEOUT)
            self.parser.add_argument(
                '-s', '--spam', type=int, help=f'Spam count (default: {DEFAULT_SPAM})', metavar='',
                default=DEFAULT_SPAM)
            self.parser.add_argument(
                '-r', '--random', type=bool, help=f'Randomize message id (default: {DEFAULT_RANDOM})', metavar='',
                default=False)
            self.parser.add_argument(
                '-a', '--accnumber', type=bool, help=f'Accession number +1 (default: {DEFAULT_AN})', metavar='',
                default=False)
            self.parser.add_argument(
                '-ct', '--curtime', type=bool, help=f'Current time (default: {DEFAULT_CUR_TIME})', metavar='',
                default=False)
        except argparse.ArgumentError or argparse.ArgumentTypeError as err:
            print(f'[HL7]: {err}')
