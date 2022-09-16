import argparse


class SysArgs():

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Running a HL7 test from the command line')
        try:
            self.parser.add_argument(
                '-i', '--ip', type=str, help='IP address or domain name to connect', metavar='')
            self.parser.add_argument(
                '-p', '--port', type=int, help='Port to connect', metavar='')
            self.parser.add_argument(
                '-t', '--timeout', type=int, help='Connection time-out', metavar='')
            self.parser.add_argument(
                '-s', '--spam', type=int, help='Spam count(0 = false)', metavar='')
            self.parser.add_argument(
                '-r', '--random', type=bool, action=argparse.BooleanOptionalAction, help='Randomize message id', metavar='')
            self.parser.add_argument(
                '-a', '--accnumber', type=bool, action=argparse.BooleanOptionalAction, help='Accession number +1', metavar='')
            self.parser.add_argument(
                '--start', type=bool, action=argparse.BooleanOptionalAction, help='Run test after program start', metavar='')
        except argparse.ArgumentError or argparse.ArgumentTypeError as err:
            print(f'[HL7]: {err}')
