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
        self.clientIP = self.getstring('Client', 'ip', fallback=self.clientIP)
        self.clientPort = self.getint('Client',
                                      'port',
                                      fallback=self.clientPort)
        self.clientTimeOut = self.getint('Client',
                                         'timeout',
                                         fallback=self.clientTimeOut)
        self.clientSpam = self.getboolean('Client',
                                          'spam',
                                          fallback=self.clientSpam)
        self.clientCountSpam = self.getint('Client',
                                           'count_spam',
                                           fallback=self.clientCountSpam)
        self.clientRandom = self.getboolean('Client',
                                            'random',
                                            fallback=self.clientRandom)
        self.clientAN = self.getboolean('Client', 'an', fallback=self.clientAN)
        self.clientHistory = self.getboolean('Client',
                                             'history_hidden',
                                             fallback=self.clientHistory)
        self.serverPort = self.getint('Server',
                                      'port',
                                      fallback=self.serverPort)
        self.serverHistory = self.getboolean('Server',
                                             'history_hidden',
                                             fallback=self.serverHistory)
        self.loadDir = self.getstring('Paths', 'load', fallback=self.loadDir)
        self.saveDir = self.getstring('Paths', 'save', fallback=self.saveDir)
        self.wrapMode = self.getboolean('Settings',
                                        'wrapmode',
                                        fallback=self.wrapMode)
        self.style = self.getstring('Settings', 'style', fallback=self.style)

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
        self.config['Server'] = {
            'port': self.serverPort,
            'history_hidden': self.serverHistory
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
