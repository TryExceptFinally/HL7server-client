from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator, QKeyEvent
from PyQt6.QtWidgets import (QVBoxLayout, QPlainTextEdit, QPushButton, QLabel,
                             QLineEdit, QGridLayout, QWidget, QTabWidget,
                             QCheckBox, QListWidget, QStatusBar, QDockWidget,
                             QMenu, QMenuBar, QWidgetAction, QMessageBox)


class Ui_MainWindow:

    def setupUi(self, root):
        # Main Window
        root.WIDTH = 1200
        root.HEIGHT = 600
        root.setWindowTitle('HL7')
        # root.setObjectName('MainWindow')
        # root.setWindowFlags(Qt.WindowType.CustomizeWindowHint | Qt.WindowType.FramelessWindowHint)

        root.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        root.setMinimumSize(root.WIDTH, root.HEIGHT)
        root.resize(root.WIDTH, root.HEIGHT)

        self.msgBox = QMessageBox()
        self.msgBox.setIcon(QMessageBox.Icon.Information)

        # Central Widget
        self.centralWidget = QWidget(root)
        self.centralWidget.setObjectName('MainWidget')

        # Main Layout
        self.centralLayout = QVBoxLayout(self.centralWidget)

        # Menu Bar
        self.menuBar = QMenuBar(self.centralWidget)

        # Menu
        self.menuFile = QMenu('File', self.menuBar)
        self.menuHistory = QMenu('History', self.menuBar)
        self.menuSettings = QMenu('Settings', self.menuBar)
        self.menuStyles = QMenu('Styles', self.menuBar)
        self.menuHelp = QMenu('Help', self.menuBar)

        # Action Menu
        # File
        self.actionExitApp = QWidgetAction(self.menuBar)
        self.actionExitApp.setText('Exit')
        # History
        self.actionClientShowHistory = QWidgetAction(self.menuBar)
        self.actionClientShowHistory.setText('Show(Client)')
        self.actionClientShowHistory.setCheckable(True)

        self.actionServerShowHistory = QWidgetAction(self.menuBar)
        self.actionServerShowHistory.setText('Show(Server)')
        self.actionServerShowHistory.setCheckable(True)
        # Styles
        self.actionDarkStyle = QWidgetAction(self.menuStyles)
        self.actionDarkStyle.setText('Dark')
        self.actionLightStyle = QWidgetAction(self.menuStyles)
        self.actionLightStyle.setText('Light')
        
        # Config
        self.actionSaveConfig = QWidgetAction(self.menuBar)
        self.actionSaveConfig.setText('Save Config')
        # WrapMode
        self.actionWrapMode = QWidgetAction(self.menuBar)
        self.actionWrapMode.setText('WrapMode')
        self.actionWrapMode.setCheckable(True)
        # Help
        self.actionHelpAbout = QWidgetAction(self.menuBar)
        self.actionHelpAbout.setText('About')
        
        self.menuFile.addAction(self.actionExitApp)
        self.menuHistory.addAction(self.actionClientShowHistory)
        self.menuHistory.addAction(self.actionServerShowHistory)
        self.menuSettings.addAction(self.actionSaveConfig)
        self.menuSettings.addAction(self.actionWrapMode)
        self.menuHelp.addAction(self.actionHelpAbout)

        self.menuStyles.addAction(self.actionLightStyle)
        self.menuStyles.addAction(self.actionDarkStyle)

        self.menuSettings.addMenu(self.menuStyles)

        self.menuBar.addMenu(self.menuFile)
        self.menuBar.addMenu(self.menuHistory)
        self.menuBar.addMenu(self.menuSettings)
        self.menuBar.addMenu(self.menuHelp)

        # Status Bar
        self.statusBar = QStatusBar(self.centralWidget)

        # Tab Widget
        self.tabWidget = QTabWidget(self.centralWidget)

        # Tabs
        self.tabClient = QWidget(self.tabWidget)
        self.tabServer = QWidget(self.tabWidget)
        # self.tabAPI = QWidget(self.tabWidget)

        # Layouts
        self.clientLayout = QGridLayout(self.tabClient)
        self.serverLayout = QGridLayout(self.tabServer)

        self.clientHistoryWidget = QWidget(self.tabClient)
        self.serverHistoryWidget = QWidget(self.tabServer)

        self.clientHistoryLayout = QGridLayout(self.clientHistoryWidget)
        self.serverHistoryLayout = QGridLayout(self.serverHistoryWidget)

        # Labels
        self.labelClientIP = QLabel('IP', self.tabClient)
        self.labelClientIP.setObjectName('titleLabel')
        self.labelClientPort = QLabel('Port', self.tabClient)
        self.labelClientPort.setObjectName('titleLabel')
        self.labelClientTimeout = QLabel('Timeout', self.tabClient)
        self.labelClientTimeout.setObjectName('titleLabel')
        self.labelClientSendInfo = QLabel(self.tabClient)
        self.labelClientSendInfo.setObjectName('statusLabel')

        self.labelServerIP = QLabel('IP', self.tabServer)
        self.labelServerIP.setObjectName('titleLabel')
        self.labelServerPort = QLabel('Port', self.tabServer)
        self.labelServerPort.setObjectName('titleLabel')
        self.labelServerClients = QLabel('Clients:', self.tabServer)
        self.labelServerClients.setObjectName('titleLabel')

        # LineEdit
        onlyInt = QIntValidator()

        self.inputClientIP = QLineEdit(self.tabClient)
        self.inputClientPort = QLineEdit(self.tabClient)
        self.inputClientPort.setValidator(onlyInt)
        self.inputClientPort.setMaxLength(5)
        self.inputClientTimeout = QLineEdit(self.tabClient)
        self.inputClientTimeout.setValidator(onlyInt)
        self.inputClientTimeout.setMaxLength(1)
        self.inputClientCountSpam = QLineEdit('0', self.tabClient)
        self.inputClientCountSpam.setValidator(onlyInt)

        self.inputServerIP = QLineEdit(self.tabServer)
        self.inputServerPort = QLineEdit(self.tabServer)
        self.inputServerPort.setValidator(onlyInt)
        self.inputServerPort.setMaxLength(5)
        self.inputServerClients = QLineEdit(self.tabServer)

        # Buttons
        self.buttonClientSend = QPushButton('SEND MESSAGE', self.tabClient)
        self.buttonClientSend.setEnabled(False)
        self.buttonClientLoad = QPushButton('LOAD FILE', self.tabClient)
        self.buttonClientSave = QPushButton('SAVE FILE', self.tabClient)
        self.buttonClientSave.setEnabled(False)
        self.buttonClientClear = QPushButton('CLEAR', self.tabClient)
        self.buttonClientHistoryClear = QPushButton('CLEAR ALL',
                                                    self.clientHistoryWidget)
        self.buttonClientHistoryClear.setEnabled(False)

        self.buttonServerHistoryClear = QPushButton('CLEAR ALL',
                                                    self.serverHistoryWidget)
        self.buttonServerHistoryClear.setEnabled(False)
        self.buttonServerListen = QPushButton('START SERVER', self.tabServer)

        # Editors
        self.editorClientOutMessage = QPlainTextEdit(self.tabClient)
        self.editorClientOutMessage.setPlaceholderText('Enter/upload outgoing message')
        self.editorClientInMessage = QPlainTextEdit(self.tabClient)

        self.editorServerOutMessage = QPlainTextEdit(self.tabServer)
        self.editorServerInMessage = QPlainTextEdit(self.tabServer)

        # CheckBox
        self.checkClientSpam = QCheckBox('SPAM', self.tabClient)
        self.checkClientRandom = QCheckBox('RANDOM', self.tabClient)
        self.checkClientAccNumber = QCheckBox('AN +1', self.tabClient)

        #  History Widget
        self.listClientHistory = HistoryWidget(self.clientHistoryWidget)
        self.listServerHistory = HistoryWidget(self.serverHistoryWidget)

        toolTip = "Press the 'Delete' button to delete the selected item"
        self.listClientHistory.setToolTip(toolTip)
        self.listServerHistory.setToolTip(toolTip)

        # Add history widget to Layout
        self.clientHistoryLayout.addWidget(self.listClientHistory)
        self.clientHistoryLayout.addWidget(self.buttonClientHistoryClear)

        self.serverHistoryLayout.addWidget(self.listServerHistory)
        self.serverHistoryLayout.addWidget(self.buttonServerHistoryClear)

        # DockWidget
        self.clientDockWidget = QDockWidget('Sending messages history',
                                            self.tabClient)
        self.clientDockWidget.setWidget(self.clientHistoryWidget)
        self.clientDockWidget.setFeatures(
            QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

        self.serverDockWidget = QDockWidget('Received messages history',
                                            self.tabServer)
        self.serverDockWidget.setWidget(self.serverHistoryWidget)
        self.serverDockWidget.setFeatures(
            QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

        # Layout addWidgets
        self.centralLayout.addWidget(self.tabWidget)

        self.clientLayout.addWidget(self.labelClientIP, 0, 0, 1, 1)
        self.clientLayout.addWidget(self.labelClientPort, 1, 0, 1, 1)
        self.clientLayout.addWidget(self.labelClientTimeout, 2, 0, 1, 1)

        self.clientLayout.addWidget(self.inputClientIP, 0, 1, 1, 1)
        self.clientLayout.addWidget(self.inputClientPort, 1, 1, 1, 1)
        self.clientLayout.addWidget(self.inputClientTimeout, 2, 1, 1, 1)
        self.clientLayout.addWidget(self.inputClientCountSpam, 0, 3, 1, 1)

        self.clientLayout.addWidget(self.checkClientSpam, 0, 2, 1, 1)
        self.clientLayout.addWidget(self.checkClientRandom, 1, 2, 1, 1)
        self.clientLayout.addWidget(self.checkClientAccNumber, 2, 2, 1, 1)

        self.clientLayout.addWidget(self.buttonClientLoad, 0, 5, 1, 1)
        self.clientLayout.addWidget(self.buttonClientSave, 1, 5, 1, 1)
        self.clientLayout.addWidget(self.buttonClientClear, 2, 5, 1, 1)
        self.clientLayout.addWidget(self.buttonClientSend, 4, 5, 1, 1)

        self.clientLayout.addWidget(self.clientDockWidget, 0, 6, 7, 1)

        self.clientLayout.addWidget(self.editorClientOutMessage, 3, 0, 1, 6)
        self.clientLayout.addWidget(self.editorClientInMessage, 5, 0, 2, 6)

        self.clientLayout.addWidget(self.labelClientSendInfo, 4, 0, 1, 5)

        self.serverLayout.addWidget(self.labelServerIP, 0, 0, 1, 1)
        self.serverLayout.addWidget(self.labelServerPort, 1, 0, 1, 1)
        self.serverLayout.addWidget(self.labelServerClients, 2, 0, 1, 1)

        self.serverLayout.addWidget(self.inputServerIP, 0, 1, 1, 1)
        self.serverLayout.addWidget(self.inputServerPort, 1, 1, 1, 1)
        self.serverLayout.addWidget(self.inputServerClients, 2, 1, 1, 1)

        self.serverLayout.addWidget(self.serverDockWidget, 0, 5, 7, 1)

        self.serverLayout.addWidget(self.editorServerOutMessage, 3, 0, 1, 4)

        self.serverLayout.addWidget(self.buttonServerListen, 4, 3, 1, 1)

        self.serverLayout.addWidget(self.editorServerInMessage, 5, 0, 2, 4)

        self.tabWidget.addTab(self.tabClient, 'CLIENT')
        self.tabWidget.addTab(self.tabServer, 'SERVER')
        # self.tabWidget.addTab(self.tabAPI, 'API')

        self.centralLayout.addWidget(self.statusBar)

        root.setCentralWidget(self.centralWidget)
        root.setMenuBar(self.menuBar)


class HistoryWidget(QListWidget):

    def __init__(self, parent) -> None:
        super().__init__(parent)

    def keyPressEvent(self, e: QKeyEvent):
        super().keyPressEvent(e)
        if e.key() == Qt.Key.Key_Delete:
            if self.currentRow() < 0:
                return
            self.takeItem(self.currentRow())
