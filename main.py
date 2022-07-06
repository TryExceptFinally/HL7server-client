import sys
import os.path

from gui import Ui_MainWindow
from PyQt6.QtGui import QIcon, QTextOption
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem
from PyQt6.QtCore import QThread, pyqtSignal, QObject

from hl7socket import ClientHL7, ServerHL7
from config import Config


def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(os.path.abspath("."), relative)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #  images
        self.setWindowIcon(QIcon(resource_path('ico.ico')))
        self.ui.buttonClientSend.setIcon(
            QIcon(resource_path('images\\send.png')))
        self.ui.buttonClientLoad.setIcon(
            QIcon(resource_path('images\\load.png')))
        self.ui.buttonClientSave.setIcon(
            QIcon(resource_path('images\\save.png')))
        self.ui.buttonClientClear.setIcon(
            QIcon(resource_path('images\\delete.png')))
        self.ui.buttonClientHistoryClear.setIcon(
            QIcon(resource_path('images\\clear.png')))
        self.ui.buttonServerHistoryClear.setIcon(
            QIcon(resource_path('images\\clear.png')))
        self.ui.buttonServerListen.setIcon(
            QIcon(resource_path('images\\listen.png')))

        #  settings
        self.ui.inputClientIP.setText(client.host)
        self.ui.inputClientPort.setText(str(client.port))
        self.ui.inputClientTimeout.setText(str(client.timeout))
        self.ui.inputClientCountSpam.setText(str(config.clientCountSpam))
        self.ui.inputServerIP.setText(server.host)
        self.ui.inputServerPort.setText(str(server.port))
        self.ui.inputServerClients.setText('Disabled')

        self.ui.inputServerIP.setReadOnly(True)
        self.ui.editorClientInMessage.setReadOnly(True)
        self.ui.editorServerInMessage.setReadOnly(True)
        self.ui.editorServerOutMessage.setReadOnly(True)

        # Config
        self.ui.checkClientSpam.setChecked(config.clientSpam)
        self.ui.checkClientRandom.setChecked(config.clientRandom)
        self.ui.checkClientAccNumber.setChecked(config.clientAN)

        self.loadDir = config.loadDir
        self.saveDir = config.saveDir

        self.ui.clientDockWidget.setHidden(config.clientHistory)
        self.ui.serverDockWidget.setHidden(config.serverHistory)

        self.ui.editorClientOutMessage.textChanged.connect(self.textChanged)

        self.ui.buttonClientLoad.clicked.connect(lambda: self.clientLoad())
        self.ui.buttonClientSave.clicked.connect(lambda: self.clientSave())
        self.ui.buttonClientClear.clicked.connect(lambda: self.clientClear())
        self.ui.buttonClientSend.clicked.connect(
            lambda: self.clientSendMessage())

        self.ui.buttonServerListen.clicked.connect(lambda: self.serverStart())

        self.ui.actionExitApp.triggered.connect(lambda: self.close())

        self.ui.actionClientShowHistory.triggered.connect(
            lambda: self.ui.clientDockWidget.setHidden(
                not self.ui.clientDockWidget.isHidden()))
        self.ui.actionClientShowHistory.setChecked(
            not self.ui.clientDockWidget.isHidden())

        self.ui.actionServerShowHistory.triggered.connect(
            lambda: self.ui.serverDockWidget.setHidden(
                not self.ui.serverDockWidget.isHidden()))
        self.ui.actionServerShowHistory.setChecked(
            not self.ui.serverDockWidget.isHidden())

        self.ui.actionWrapMode.triggered.connect(
            lambda: self.wrapModeChanged())
        self.ui.actionWrapMode.setChecked(config.wrapMode)
        self.wrapModeChanged()

        self.ui.actionSaveConfig.triggered.connect(lambda: self.configSave())
        self.ui.actionHelpAbout.triggered.connect(lambda: self.msgAbout())
        self.serverThreadListen = SocketThread(self.serverStartListen)
        self.serverThreadListen.signals.finished.connect(self.serverStopListen)
        self.serverThreadListen.signals.result.connect(self.serverResultListen)

        self.clientThreadSending = SocketThread(self.clientStartSending)
        self.clientThreadSending.signals.finished.connect(
            self.clientStopSending)
        self.clientThreadSending.signals.result.connect(
            self.clientResultSending)

        self.ui.listClientHistory.itemClicked.connect(
            lambda: self.resultItemMessages(
                self.ui.editorClientInMessage, self.ui.editorClientOutMessage,
                self.ui.listClientHistory.currentItem()))
        self.ui.listServerHistory.itemClicked.connect(
            lambda: self.resultItemMessages(
                self.ui.editorServerInMessage, self.ui.editorServerOutMessage,
                self.ui.listServerHistory.currentItem()))

        self.ui.listClientHistory.model().rowsInserted.connect(
            lambda: self.historyChanged(self.ui.listClientHistory, self.ui.
                                        buttonClientHistoryClear))
        self.ui.listClientHistory.model().rowsRemoved.connect(
            lambda: self.historyChanged(self.ui.listClientHistory, self.ui.
                                        buttonClientHistoryClear))

        self.ui.listServerHistory.model().rowsInserted.connect(
            lambda: self.historyChanged(self.ui.listServerHistory, self.ui.
                                        buttonServerHistoryClear))
        self.ui.listServerHistory.model().rowsRemoved.connect(
            lambda: self.historyChanged(self.ui.listClientHistory, self.ui.
                                        buttonServerHistoryClear))

        self.ui.buttonClientHistoryClear.clicked.connect(
            lambda: self.clearItems(self.ui.listClientHistory, self.ui.
                                    buttonClientHistoryClear))
        self.ui.buttonServerHistoryClear.clicked.connect(
            lambda: self.clearItems(self.ui.listServerHistory, self.ui.
                                    buttonServerHistoryClear))

    # Root Events
    def closeEvent(self, event):
        self.configSave()

    # messagebox
    def msgAbout(self):
        self.ui.msgBox.setText('HL7 client and server')
        self.ui.msgBox.setWindowTitle('LINS')
        self.ui.msgBox.exec()

    # historyChanged
    def historyChanged(self, listHistory, buttonHistory):
        buttonHistory.setEnabled(listHistory.count())

    # Wrap Mode Changed
    def wrapModeChanged(self):
        if self.ui.actionWrapMode.isChecked():
            wrapMode = QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere
        else:
            wrapMode = QTextOption.WrapMode.NoWrap

        self.ui.editorClientOutMessage.setWordWrapMode(wrapMode)
        self.ui.editorClientInMessage.setWordWrapMode(wrapMode)

        self.ui.editorServerOutMessage.setWordWrapMode(wrapMode)
        self.ui.editorServerInMessage.setWordWrapMode(wrapMode)

        config.wrapMode = self.ui.actionWrapMode.isChecked()

    # textChanged
    def textChanged(self):
        enabled = self.ui.editorClientOutMessage.toPlainText() != ''
        self.ui.buttonClientSend.setEnabled(enabled)
        self.ui.buttonClientSave.setEnabled(enabled)

    # Result clicked item history
    def resultItemMessages(self, inMsg, outMsg, data):
        inMsg.setPlainText(data.inMsg)
        outMsg.setPlainText(data.outMsg)
        if data.sendInfo:
            self.ui.labelClientSendInfo.setText(data.sendInfo)

    def clearItems(self, listHistory, buttonHistory):
        listHistory.clear()
        buttonHistory.setEnabled(False)
        self.ui.statusBar.showMessage('History clear', 5000)

    def configSave(self):
        config.clientIP = self.ui.inputClientIP.text()
        config.clientPort = self.ui.inputClientPort.text()
        config.clientTimeOut = self.ui.inputClientTimeout.text()
        config.clientSpam = self.ui.checkClientSpam.isChecked()
        config.clientCountSpam = self.ui.inputClientCountSpam.text()
        config.clientRandom = self.ui.checkClientRandom.isChecked()
        config.clientAN = self.ui.checkClientAccNumber.isChecked()
        config.clientHistory = self.ui.clientDockWidget.isHidden()
        config.serverPort = self.ui.inputServerPort.text()
        config.serverHistory = self.ui.serverDockWidget.isHidden()
        config.loadDir = self.loadDir
        config.saveDir = self.saveDir
        config.save()
        print('[CONFIG]: Config save')

    def clientLoad(self):
        file = QFileDialog.getOpenFileName(self, 'Load HL7 message',
                                           self.loadDir,
                                           'HL7 files (*.txt *.hl7)')[0]
        if not file:
            return
        self.loadDir = file
        self.ui.statusBar.showMessage(f'File: "{self.loadDir}" loaded.')
        try:
            with open(file, encoding=client.code, mode='r') as f:
                data = f.read()
                self.ui.editorClientOutMessage.setPlainText(data)
        except Exception as exp:
            print(exp)

    def clientSave(self):
        file = QFileDialog.getSaveFileName(self, 'Save HL7 message',
                                           self.saveDir,
                                           'HL7 files (*.txt *.hl7)')[0]
        if not file:
            return
        self.saveDir = file
        self.ui.statusBar.showMessage(f'File: "{self.saveDir}" saved.')
        try:
            with open(file, encoding=client.code, mode='w') as f:
                data = self.ui.editorClientOutMessage.toPlainText()
                f.write(data)
        except Exception as exp:
            print(exp)

    def clientClear(self):
        self.ui.editorClientInMessage.setPlainText('')
        self.ui.editorClientOutMessage.setPlainText('')
        self.ui.labelClientSendInfo.setText('')
        self.ui.statusBar.showMessage('Clear', 5000)

    def clientSendMessage(self):
        if not client.run:
            if not self.ui.inputClientTimeout.text().isdigit():
                self.ui.inputClientTimeout.setText('1')
            client.outMsg = self.ui.editorClientOutMessage.toPlainText()
            client.host = self.ui.inputClientIP.text()
            client.port = int(self.ui.inputClientPort.text())
            client.timeout = int(self.ui.inputClientTimeout.text())
            client.accNumber = self.ui.checkClientAccNumber.isChecked()
            client.random = self.ui.checkClientRandom.isChecked()
            self.clientThreadSending.start()
            self.ui.statusBar.showMessage('Sending...')
            self.ui.buttonClientSend.setText('STOP SENDING MESSAGE')
            self.ui.editorClientOutMessage.setReadOnly(True)
            client.run = True
        else:
            client.run = False

    def clientStartSending(self) -> str:
        tAllRecv = 0.0
        countMsg = 0
        limitSpam = 1
        if self.ui.checkClientSpam.isChecked():
            limitSpam = int(self.ui.inputClientCountSpam.text())
        while client.run and (countMsg < limitSpam):
            countMsg += 1
            timeMsg, tSendEnd, tRecvEnd = client.sendHL7()
            tAllRecv += tRecvEnd
            self.clientThreadSending.signals.result.emit(
                timeMsg,
                f'№{countMsg}, Sending: {tSendEnd:.5f}, Received: {tRecvEnd:.5f}'
            )
        return f'Average time received {countMsg} messages: {tAllRecv/countMsg:.5f}'

    def clientResultSending(self, timeMsg: str, result: str):
        if not client.inMsg:
            print('[CLIENT]: Empty response received from server')
            # self.ui.statusBar.showMessage('Empty response received from server', 3000)
        self.ui.editorClientInMessage.setPlainText(client.inMsg)
        self.ui.editorClientOutMessage.setPlainText(client.outMsg)
        self.ui.labelClientSendInfo.setText(result)
        text = f'[{timeMsg}]: To {client.host}:{client.port}'
        msg = DataItems(self.ui.editorClientInMessage.toPlainText(),
                        self.ui.editorClientOutMessage.toPlainText(),
                        self.ui.labelClientSendInfo.text())
        msg.setText(text)
        self.ui.listClientHistory.addItem(msg)

    def clientStopSending(self, result: str):
        self.ui.statusBar.showMessage(result)
        self.ui.buttonClientSend.setText('SEND MESSAGE')
        self.ui.editorClientOutMessage.setReadOnly(False)
        client.run = False

    def serverStart(self):
        if not server.run:
            server.outMsg = self.ui.editorServerOutMessage.toPlainText()
            server.port = int(self.ui.inputServerPort.text())
            server.createServer()
            server.run = True
            self.serverThreadListen.start()
            self.ui.editorServerInMessage.setPlainText('')
            self.ui.buttonServerListen.setText('STOP SERVER')
            self.ui.editorServerOutMessage.setReadOnly(True)
        else:
            server.run = False
            server.close(server.sock)

    def serverStartListen(self):
        while server.run:
            timeMsg, result = server.listen()
            self.serverThreadListen.signals.result.emit(timeMsg, result)

    def serverResultListen(self, timeMsg: str, result: str):
        if not server.inMsg:
            self.ui.statusBar.showMessage('Empty message received from client',
                                          3000)
            return
        self.ui.editorServerInMessage.setPlainText(server.inMsg)
        self.ui.editorServerOutMessage.setPlainText(server.outMsg)
        text = f'[{timeMsg}]: From {result}'
        msg = DataItems(self.ui.editorServerInMessage.toPlainText(),
                        self.ui.editorServerOutMessage.toPlainText(), '')
        msg.setText(text)
        self.ui.listServerHistory.addItem(msg)

    def serverStopListen(self):
        self.ui.statusBar.showMessage('Server closed', 3000)
        self.ui.buttonServerListen.setText('START SERVER')
        self.ui.editorServerOutMessage.setReadOnly(False)


class DataItems(QListWidgetItem):

    def __init__(self, inMsg: str, outMsg: str, sendInfo: str):
        super().__init__()
        self.inMsg = inMsg
        self.outMsg = outMsg
        self.sendInfo = sendInfo


class SocketSignals(QObject):
    finished = pyqtSignal(str)
    result = pyqtSignal(str, str)


class SocketThread(QThread):

    def __init__(self, fn):
        super().__init__()
        self.signals = SocketSignals()
        self.fn = fn

    def run(self):
        result = self.fn()
        self.signals.finished.emit(result)


config = Config('config.ini')
config.load()

client = ClientHL7(config.clientIP, config.clientPort, config.clientTimeOut)
server = ServerHL7('127.0.0.1', config.serverPort)

app = QApplication(sys.argv)
root = MainWindow()

stylesheet = resource_path('styles\\style_gui.qss')
with open(stylesheet, 'r') as ss:
    root.setStyleSheet(ss.read())
root.show()

sys.exit(app.exec())
