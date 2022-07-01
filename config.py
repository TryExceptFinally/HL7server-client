import configparser


class Config:

    def __init__(self, ini: str):
        
        self.ini = ini
        self.config = configparser.ConfigParser()
        self.clientIP: str = '127.0.0.1'
        self.clientPort: int = 6005
        self.clientTimeOut: int = 3
        self.clientSpam: bool = False
        self.clientCountSpam: int = 0
        self.clientRandom: bool = False
        self.clientAN: bool = False
        self.clientHistory: bool = False
        self.serverPort: int = 6005
        self.loadDir: str = './'
        self.saveDir: str = './message.hl7'

    def load(self):
        self.config.read(self.ini)
        self.clientIP = self.config.get('Client', 'ip', fallback=self.clientIP)
        self.clientPort = self.config.getint('Client',
                                             'port',
                                             fallback=self.clientPort)
        self.clientTimeOut = self.config.getint('Client',
                                                'timeout',
                                                fallback=self.clientTimeOut)
        self.clientSpam = self.config.getboolean('Client',
                                                 'spam',
                                                 fallback=self.clientSpam)
        self.clientCountSpam = self.config.getint(
            'Client', 'count_spam', fallback=self.clientCountSpam)
        self.clientRandom = self.config.getboolean('Client',
                                                   'random',
                                                   fallback=self.clientRandom)
        self.clientAN = self.config.getboolean('Client',
                                               'an',
                                               fallback=self.clientAN)
        self.clientHistory = self.config.getboolean(
            'Client', 'history_hidden', fallback=self.clientHistory)
        self.serverPort = self.config.getint('Server',
                                             'port',
                                             fallback=self.serverPort)
        self.loadDir = self.config.get('Paths', 'load', fallback=self.loadDir)
        self.saveDir = self.config.get('Paths', 'save', fallback=self.saveDir)

    def save(self):
        self.config['Client'] = {
            'ip': self.clientIP,
            'port': self.clientPort,
            'timeout': self.clientTimeOut,
            'spam': self.clientSpam,
            'count_spam': self.clientCountSpam,
            'random': self.clientRandom,
            'an': self.clientAN,
            'history_hidden': self.clientHistory
        }
        self.config['Server'] = {'port': self.serverPort}
        self.config['Paths'] = {'load': self.loadDir, 'save': self.saveDir}
        with open(self.ini, 'w') as configfile:
            try:
                self.config.write(configfile)
            except OSError:
                print(f'[CONFIG]: Error save file: {self.ini}')
