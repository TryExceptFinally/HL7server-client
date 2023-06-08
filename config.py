import configparser


class Config:

    def __init__(self, ini: str):
        self.ini = ini
        self.config = configparser.ConfigParser()
        self.clientAddresses: str = '127.0.0.1:6005'
        self.clientLastAddress: int = 0
        self.clientTimeOut: int = 3
        self.clientSpam: bool = False
        self.clientCountSpam: int = 0
        self.clientRandom: bool = False
        self.clientAN: bool = False
        self.clientCurrentTime: bool = False
        self.clientHistory: bool = False
        self.serverPort: int = 6005
        self.serverHistory: bool = False
        self.loadDir: str = './'
        self.saveDir: str = './message.hl7'
        self.wrapMode: bool = True
        self.style: str = 'dark'

    def getstring(self, section, option, fallback):
        string = self.config.get(section, option, fallback=fallback)
        if string:
            return string
        else:
            return fallback

    def getint(self, section, option, fallback):
        try:
            return self.config.getint(section, option, fallback=fallback)
        except ValueError:
            return fallback

    def getboolean(self, section, option, fallback):
        try:
            return self.config.getboolean(section, option, fallback=fallback)
        except ValueError:
            return fallback

    def load(self):
        self.config.read(self.ini)
        self.clientAddresses = self.getstring('Client', 'addresses', fallback=self.clientAddresses)
        self.clientLastAddress = self.getint('Client', 'last_address', fallback=self.clientLastAddress)
        self.clientTimeOut = self.getint('Client', 'timeout', fallback=self.clientTimeOut)
        self.clientSpam = self.getboolean('Client', 'spam', fallback=self.clientSpam)
        self.clientCountSpam = self.getint('Client', 'count_spam', fallback=self.clientCountSpam)
        self.clientRandom = self.getboolean('Client', 'random', fallback=self.clientRandom)
        self.clientAN = self.getboolean('Client', 'an', fallback=self.clientAN)
        self.clientCurrentTime = self.getboolean('Client', 'time', fallback=self.clientCurrentTime)
        self.clientHistory = self.getboolean('Client', 'history', fallback=self.clientHistory)
        self.serverPort = self.getint('Server', 'port', fallback=self.serverPort)
        self.serverHistory = self.getboolean('Server', 'history', fallback=self.serverHistory)
        self.loadDir = self.getstring('Paths', 'load', fallback=self.loadDir)
        self.saveDir = self.getstring('Paths', 'save', fallback=self.saveDir)
        self.wrapMode = self.getboolean('Settings', 'wrapmode', fallback=self.wrapMode)
        self.style = self.getstring('Settings', 'style', fallback=self.style)

    def save(self):
        self.config['Client'] = {
            'addresses': self.clientAddresses,
            'last_address': self.clientLastAddress,
            'timeout': self.clientTimeOut,
            'spam': self.clientSpam,
            'count_spam': self.clientCountSpam,
            'random': self.clientRandom,
            'an': self.clientAN,
            'time': self.clientCurrentTime,
            'history': self.clientHistory
        }
        self.config['Server'] = {
            'port': self.serverPort,
            'history': self.serverHistory
        }
        self.config['Paths'] = {'load': self.loadDir, 'save': self.saveDir}
        self.config['Settings'] = {
            'wrapmode': self.wrapMode,
            'style': self.style
        }
        with open(self.ini, 'w') as configfile:
            try:
                self.config.write(configfile)
            except OSError:
                print(f'[CONFIG]: Error save file: {self.ini}')
