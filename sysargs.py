import argparse


class SysArgs():

    def __init__(self):
        DFLT_PORT = 6005
        DFLT_TIMEOUT = 3
        DFLT_SPAM = 1
        DFLT_RANDOM = False
        DFLT_AN = False
        self.parser = argparse.ArgumentParser(
            description='Running a HL7 test from the command line')
        try:
            self.parser.add_argument(
                '-fp', '--filepath', type=str, help='Path to HL7 file', metavar='', required=True)
            self.parser.add_argument(
                '-i', '--ip', type=str, help='IP address or domain name to connect', metavar='', required=True)
            self.parser.add_argument(
                '-p', '--port', type=int, help=f'Port to connect (default: {DFLT_PORT})', metavar='', default=DFLT_PORT)
            self.parser.add_argument(
                '-t', '--timeout', type=int, help=f'Connection time-out (default: {DFLT_TIMEOUT})', metavar='', default=DFLT_TIMEOUT)
            self.parser.add_argument(
                '-s', '--spam', type=int, help=f'Spam count (default: {DFLT_SPAM})', metavar='', default=DFLT_SPAM)
            self.parser.add_argument(
                '-r', '--random', type=bool, help=f'Randomize message id (default: {DFLT_RANDOM})', metavar='', default=False)
            self.parser.add_argument(
                '-a', '--accnumber', type=bool, help=f'Accession number +1 (default: {DFLT_AN})', metavar='', default=False)
        except argparse.ArgumentError or argparse.ArgumentTypeError as err:
            print(f'[HL7]: {err}')
