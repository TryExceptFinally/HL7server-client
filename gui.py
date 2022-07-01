from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (QVBoxLayout, QPlainTextEdit, QPushButton, QLabel,
                             QLineEdit, QGridLayout, QWidget, QTabWidget,
                             QCheckBox, QListWidget, QStatusBar, QDockWidget,
                             QMenu, QMenuBar, QWidgetAction, QMessageBox)

stylesheet = '''

#MainWidget {
    background: #060122;
    color: white;
}

QStatusBar {
    font: 13px;
}

QDockWidget {
    color: white;
    font: bold 14px;
    background: #060122;
    max-width: 340px;
}

QDockWidget::title {
    background: #1f2b3a;
    border: 1px solid #2a71a7;
    border-radius: 5px;
    text-align: center;
}

QDockWidget::close-button {
    background: white;
    border: 1px solid #2a71a7;
    border-radius: 5px;
    subcontrol-position: top right;
    subcontrol-origin: margin;
    top: 2px; right: 2px;
}

QDockWidget::close-button:hover {
    background: #fa3232;
}

QMenuBar {
    color: white;
    background: #1f2b3a;
    border-bottom: 1px solid #3a5199;
}

QMenuBar::item {
    background: transparent;
}

QMenuBar::item:selected {
    background: #3a5199;
}

QMenuBar::item:pressed {
    background: #2a71a7;
}

QMenu {
    color: white;
    background: #1f2b3a;
    border: 1px solid #3a5199;
}

QMenu::item:selected {
    background: #337bae;
}

QPlainTextEdit {
    color: white;
    background: #1f2b3a;
    border: 1px solid #2a71a7;
    font: bold 13px;
    border-radius: 5px;
    padding: 1 1px;
}

QPlainTextEdit[readOnly="true"] { border: 1px solid gray }

QLabel#statusLabel {
    font: 14px;
    color: white;
    border-top: none;
}

QLabel#titleLabel {
    font: bold 14px;
    color: white;
    min-width: 5em;
    max-width: 5em;
    min-height: 1em;
    padding: 0 10px;
    border-top: 1px solid #063852;
}

QLineEdit { 
    color: white;
    background: #1f2b3a;
    font: 15px;
    border: 1px solid #2a71a7;
    border-radius: 5px; 
    height: 1em;
    min-width: 9em;
    max-width: 9em;
    padding: 3 3px;
}

QLineEdit[readOnly="true"] { border: 1px solid gray }

QPushButton {
    color: white;
    background: #3a5199;
    border: 1px solid #111bae;
    border-style: outset;
    border-radius: 5px;
    font: bold 14px;
    min-width: 10em;
    max-width: 320px;
    height: 1em;
    padding: 3 3px;
}

QPushButton:hover {
    border: 1px solid #337bae;
    border-style: outset;
}

QPushButton:pressed {
    background: #337bae;
    border-style: inset;
}

QPushButton:!enabled {
    color: lightgray;
}

QCheckBox {
    width: 100px;
}

QStatusBar {
    color: white;
}

QTabWidget::pane {
    border-top: 2px solid #063852;
}

QTabBar::tab {
    color: white;
    background: #3a5199; 
    border: 2px solid #063852;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    padding: 0 10px;
    font: bold 14px;
}

QTabBar::tab:selected {
    background: #337bae;
}

QTabBar::tab:!selected {
    margin-top: 4px;
}

QCheckBox {
    color: white;
    max-width: 5em;
}

QListWidget {
    background: #1f2b3a;
    border-radius: 5px;
    border: 1px solid #2a71a7;
    font: 16px;
    color: white;
    min-width: 320px;
}

'''


class Ui_MainWindow:

    def setupUi(self, root):
        #Main Window
        root.WIDTH = 1200
        root.HEIGHT = 600
        root.setWindowTitle('HL7')
        #root.setObjectName('MainWindow')
        #root.setWindowFlags(Qt.WindowType.CustomizeWindowHint | Qt.WindowType.FramelessWindowHint)
        root.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        root.setMinimumSize(root.WIDTH, root.HEIGHT)
        root.resize(root.WIDTH, root.HEIGHT)

        #stylesheet
        self.stylesheet = stylesheet

        self.msgBox = QMessageBox()
        self.msgBox.setIcon(QMessageBox.Icon.Information)

        #Central Widget
        self.centralWidget = QWidget(root)
        self.centralWidget.setObjectName('MainWidget')

        #Main Layout
        self.centralLayout = QVBoxLayout(self.centralWidget)

        #Menu Bar
        self.menuBar = QMenuBar(self.centralWidget)

        #Menu
        self.menuFile = QMenu('File', self.menuBar)
        self.menuHistory = QMenu('History', self.menuBar)
        self.menuConfig = QMenu('Config', self.menuBar)
        self.menuHelp = QMenu('Help', self.menuBar)

        #Action Menu
        #File
        self.actionExitApp = QWidgetAction(self.menuBar)
        self.actionExitApp.setText('Exit')
        #History
        self.actionShowHideHistory = QWidgetAction(self.menuBar)
        self.actionShowHideHistory.setText('Show/Hide')
        #Config
        self.actionSaveConfig = QWidgetAction(self.menuBar)
        self.actionSaveConfig.setText('Save')
        #Help
        self.actionHelpAbout = QWidgetAction(self.menuBar)
        self.actionHelpAbout.setText('About')

        self.menuFile.addAction(self.actionExitApp)
        self.menuHistory.addAction(self.actionShowHideHistory)
        self.menuConfig.addAction(self.actionSaveConfig)
        self.menuHelp.addAction(self.actionHelpAbout)

        self.menuBar.addMenu(self.menuFile)
        self.menuBar.addMenu(self.menuHistory)
        self.menuBar.addMenu(self.menuConfig)
        self.menuBar.addMenu(self.menuHelp)

        #Status Bar
        self.statusBar = QStatusBar(self.centralWidget)

        #Tab Widget
        self.tabWidget = QTabWidget(self.centralWidget)

        #Tabs
        self.tabClient = QWidget(self.tabWidget)
        self.tabServer = QWidget(self.tabWidget)
        #self.tabAPI = QWidget(self.tabWidget)

        #Layouts
        self.clientLayout = QGridLayout(self.tabClient)
        self.serverLayout = QGridLayout(self.tabServer)

        self.clientHistoryWidget = QWidget(self.tabClient)
        self.serverHistoryWidget = QWidget(self.tabServer)

        self.clientHistoryLayout = QGridLayout(self.clientHistoryWidget)
        self.serverHistoryLayout = QGridLayout(self.serverHistoryWidget)

        #Labels
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

        #LineEdit
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

        #Buttons
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

        #Editors
        self.editorClientOutMessage = QPlainTextEdit(self.tabClient)
        self.editorClientInMessage = QPlainTextEdit(self.tabClient)

        self.editorServerOutMessage = QPlainTextEdit(self.tabServer)
        self.editorServerInMessage = QPlainTextEdit(self.tabServer)

        #CheckBox
        self.checkClientSpam = QCheckBox('SPAM', self.tabClient)
        self.checkClientRandom = QCheckBox('RANDOM', self.tabClient)
        self.checkClientAccNumber = QCheckBox('AN +1', self.tabClient)

        # History Widget
        self.listClientHistory = QListWidget(self.clientHistoryWidget)
        self.listServerHistory = QListWidget(self.serverHistoryWidget)

        toolTip = "Press the 'Delete' button to delete the selected item"
        self.listClientHistory.setToolTip(toolTip)
        self.listServerHistory.setToolTip(toolTip)

        #Add history widget to Layout
        self.clientHistoryLayout.addWidget(self.listClientHistory)
        self.clientHistoryLayout.addWidget(self.buttonClientHistoryClear)

        self.serverHistoryLayout.addWidget(self.listServerHistory)
        self.serverHistoryLayout.addWidget(self.buttonServerHistoryClear)

        #DockWidget
        self.clientDockWidget = QDockWidget('Sending messages history',
                                            self.tabClient)
        self.clientDockWidget.setWidget(self.clientHistoryWidget)
        self.clientDockWidget.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetClosable)

        self.serverDockWidget = QDockWidget('Received messages history',
                                            self.tabServer)
        self.serverDockWidget.setWidget(self.serverHistoryWidget)
        self.serverDockWidget.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetClosable)

        #Layout addWidgets
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
        #self.tabWidget.addTab(self.tabAPI, 'API')

        self.centralLayout.addWidget(self.statusBar)

        root.setCentralWidget(self.centralWidget)
        root.setMenuBar(self.menuBar)