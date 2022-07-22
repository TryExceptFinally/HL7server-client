from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QIntValidator, QKeyEvent, QActionGroup
from PyQt6.QtWidgets import (QVBoxLayout, QPlainTextEdit, QPushButton, QLabel,
                             QLineEdit, QGridLayout, QWidget, QTabWidget,
                             QCheckBox, QListWidget, QStatusBar, QDockWidget,
                             QMenu, QMenuBar, QWidgetAction, QMessageBox,
                             QSplitter, QRadioButton, QButtonGroup)


class Ui_MainWindow:

    def setupUi(self, root):
        # Main Window
        minWidth = 1200
        minHeight = 600
        # root.setWindowTitle('HL7')
        # root.setObjectName('MainWindow')
        # root.setWindowFlags(Qt.WindowType.CustomizeWindowHint | Qt.WindowType.FramelessWindowHint)

        root.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        root.setMinimumSize(minWidth, minHeight)

        self.getSettingsValues()
        rWidth = self.settingsWindow.value('width', minWidth)
        rHeight = self.settingsWindow.value('height', minHeight)
        root.resize(rWidth, rHeight)

        self.msgBox = QMessageBox(root)
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
        self.actionStylesGroup = QActionGroup(self.menuStyles)
        self.actionStylesGroup.setExclusive(True)

        self.actionDarkStyle = QWidgetAction(self.menuStyles)
        self.actionDarkStyle.setText('Dark')
        self.actionDarkStyle.setCheckable(True)
        self.actionLightStyle = QWidgetAction(self.menuStyles)
        self.actionLightStyle.setText('Light')
        self.actionLightStyle.setCheckable(True)

        self.actionStylesGroup.addAction(self.actionDarkStyle)
        self.actionStylesGroup.addAction(self.actionLightStyle)

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
        self.statusBar.setSizeGripEnabled(False)

        # Tab Widget
        self.tabWidget = QTabWidget(self.centralWidget)

        # Tabs
        self.tabClient = QWidget(self.tabWidget)
        self.tabServer = QWidget(self.tabWidget)

        self.clientLayout = QGridLayout(self.tabClient)
        self.serverLayout = QGridLayout(self.tabServer)

        self.clientOutgoingWidget = QWidget(self.tabClient)
        self.clientOutgoingLayout = QGridLayout(self.clientOutgoingWidget)
        self.clientOutgoingLayout.setContentsMargins(0, 0, 0, 5)

        self.clientHistoryWidget = QWidget(self.tabClient)
        self.clientHistoryLayout = QGridLayout(self.clientHistoryWidget)
        self.clientHistoryLayout.setContentsMargins(0, 1, 0, 0)

        self.serverOutgoingWidget = QWidget(self.tabServer)
        self.serverOutgoingLayout = QGridLayout(self.serverOutgoingWidget)
        self.serverOutgoingLayout.setContentsMargins(0, 0, 0, 5)

        self.serverHistoryWidget = QWidget(self.tabServer)
        self.serverHistoryLayout = QGridLayout(self.serverHistoryWidget)
        self.serverHistoryLayout.setContentsMargins(0, 1, 0, 0)

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

        self.buttonServerClear = QPushButton('CLEAR', self.tabServer)
        self.buttonServerHistoryClear = QPushButton('CLEAR ALL',
                                                    self.serverHistoryWidget)
        self.buttonServerHistoryClear.setEnabled(False)

        self.buttonServerListen = QPushButton('START SERVER', self.tabServer)

        # Editors
        self.editorClientOutMessage = QPlainTextEdit(self.tabClient)
        self.editorClientOutMessage.setPlaceholderText(
            'Enter/upload outgoing message')
        self.editorClientInMessage = QPlainTextEdit(self.tabClient)

        self.editorServerOutMessage = QPlainTextEdit(self.tabServer)
        self.editorServerInMessage = QPlainTextEdit(self.tabServer)

        # CheckBox
        self.checkClientSpam = QCheckBox('SPAM', self.tabClient)
        self.checkClientRandom = QCheckBox('RANDOM', self.tabClient)
        self.checkClientAccNumber = QCheckBox('AN +1', self.tabClient)

        # Radio Button group
        self.radioBtServerAA = QRadioButton('AA - Accept', self.tabServer)
        self.radioBtServerAA.setChecked(True)
        self.radioBtServerAR = QRadioButton('AR - Reject', self.tabServer)
        self.radioBtServerAE = QRadioButton('AE - Error', self.tabServer)

        self.radioBtServerGroup = QButtonGroup(self.tabServer)
        self.radioBtServerGroup.addButton(self.radioBtServerAA)
        self.radioBtServerGroup.addButton(self.radioBtServerAR)
        self.radioBtServerGroup.addButton(self.radioBtServerAE)

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

        # Add OutgoingLayout
        self.clientOutgoingLayout.addWidget(self.editorClientOutMessage, 0, 0,
                                            1, 2)
        self.clientOutgoingLayout.addWidget(self.labelClientSendInfo, 1, 0, 1,
                                            1)
        self.clientOutgoingLayout.addWidget(self.buttonClientSend, 1, 1, 1, 1)

        self.serverOutgoingLayout.addWidget(self.editorServerOutMessage, 0, 0,
                                            1, 2)
        self.serverOutgoingLayout.addWidget(self.buttonServerListen, 1, 1, 1,
                                            1)

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

        # Splitters
        self.clientEditorsSplitter = QSplitter(Qt.Orientation.Vertical)
        self.clientEditorsSplitter.addWidget(self.clientOutgoingWidget)
        self.clientEditorsSplitter.addWidget(self.editorClientInMessage)
        self.clientEditorsSplitter.setHandleWidth(1)
        self.clientEditorsSplitter.setCollapsible(0, False)
        self.clientEditorsSplitter.setCollapsible(1, False)

        self.serverEditorsSplitter = QSplitter(Qt.Orientation.Vertical)
        self.serverEditorsSplitter.addWidget(self.serverOutgoingWidget)
        self.serverEditorsSplitter.addWidget(self.editorServerInMessage)
        self.serverEditorsSplitter.setHandleWidth(1)
        self.serverEditorsSplitter.setCollapsible(0, False)
        self.serverEditorsSplitter.setCollapsible(1, False)

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

        self.clientLayout.addWidget(self.clientEditorsSplitter, 3, 0, 2, 6)

        self.clientLayout.addWidget(self.clientDockWidget, 0, 6, 5, 1)
        # self.clientLayout.addWidget(self.editorClientInMessage, 4, 0, 1, 6)

        self.serverLayout.addWidget(self.labelServerIP, 0, 0, 1, 1)
        self.serverLayout.addWidget(self.labelServerPort, 1, 0, 1, 1)
        self.serverLayout.addWidget(self.labelServerClients, 2, 0, 1, 1)

        self.serverLayout.addWidget(self.inputServerIP, 0, 1, 1, 1)
        self.serverLayout.addWidget(self.inputServerPort, 1, 1, 1, 1)
        self.serverLayout.addWidget(self.inputServerClients, 2, 1, 1, 1)

        self.serverLayout.addWidget(self.radioBtServerAA, 0, 2, 1, 1)
        self.serverLayout.addWidget(self.radioBtServerAR, 1, 2, 1, 1)
        self.serverLayout.addWidget(self.radioBtServerAE, 2, 2, 1, 1)

        self.serverLayout.addWidget(self.buttonServerClear, 2, 4, 1, 1)

        self.serverLayout.addWidget(self.serverEditorsSplitter, 3, 0, 1, 5)

        self.serverLayout.addWidget(self.serverDockWidget, 0, 5, 4, 1)

        self.tabWidget.addTab(self.tabClient, 'CLIENT')
        self.tabWidget.addTab(self.tabServer, 'SERVER')
        # self.tabWidget.addTab(self.tabAPI, 'API')

        self.centralLayout.addWidget(self.statusBar)

        root.setCentralWidget(self.centralWidget)
        root.setMenuBar(self.menuBar)

    def getSettingsValues(self):
        self.settingsWindow = QSettings('HL7 CS', 'Window size')


class HistoryWidget(QListWidget):

    def __init__(self, parent) -> None:
        super().__init__(parent)

    def keyPressEvent(self, e: QKeyEvent):
        super().keyPressEvent(e)
        if e.key() == Qt.Key.Key_Delete:
            if self.currentRow() < 0:
                return
            self.takeItem(self.currentRow())
