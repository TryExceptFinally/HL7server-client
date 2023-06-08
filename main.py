import sys
import os.path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QTextOption, QCursor
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem
from PyQt6.QtCore import QEvent, QThread, pyqtSignal, QObject

from gui_elements import Ui_MainWindow
from config import Config
from hl7socket import ClientHL7, ServerHL7


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # images
        self.setWindowIcon(QIcon(resourcePath('ico.ico')))
        self.ui.buttonClientSend.setIcon(
            QIcon(resourcePath('images\\send.png')))
        self.ui.buttonClientLoad.setIcon(
            QIcon(resourcePath('images\\load.png')))
        self.ui.buttonClientSave.setIcon(
            QIcon(resourcePath('images\\save.png')))
        self.ui.buttonClientClear.setIcon(
            QIcon(resourcePath('images\\delete.png')))
        self.ui.buttonServerClear.setIcon(
            QIcon(resourcePath('images\\delete.png')))
        self.ui.buttonClientHistoryClear.setIcon(
            QIcon(resourcePath('images\\clear.png')))
        self.ui.buttonServerHistoryClear.setIcon(
            QIcon(resourcePath('images\\clear.png')))
        self.ui.buttonServerListen.setIcon(
            QIcon(resourcePath('images\\listen.png')))

        #  settings

        client_address = config.clientAddresses.split(",")
        self.client_address = {}

        for address in client_address:
            address = address.split(":")
            if len(address) == 2:
                self.client_address[address[0]] = address[1]

        self.ui.cboxClientHosts.addItems(self.client_address.keys())
        self.ui.cboxClientHosts.customContextMenuRequested.connect(self.popupClientAddresses)
        self.ui.cboxClientHosts.currentIndexChanged.connect(self.client_set_port_by_host)
        self.ui.cboxClientHosts.setCurrentIndex(config.clientLastAddress)
        self.client_set_port_by_host()

        self.ui.actionDeleteHost.triggered.connect(lambda: self.deleteClientHost())

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
        self.ui.checkClientCurrentTime.setChecked(config.clientCurrentTime)

        self.loadDir = config.loadDir
        self.saveDir = config.saveDir

        self.ui.editorClientOutMessage.textChanged.connect(self.textChanged)
        self.ui.editorClientOutMessage.cursorPositionChanged.connect(
            self.cursorPosition)

        self.ui.labelClientSendInfo.installEventFilter(self)
        self.ui.cboxClientHosts.installEventFilter(self)
        self.ui.inputClientPort.installEventFilter(self)
        # self.ui.labelClientSendInfo.setClickable(True)
        # self.ui.labelClientSendInfo.clicked.connect(lambda: print('12421'))

        self.ui.buttonClientLoad.clicked.connect(lambda: self.clientLoad())
        self.ui.buttonClientSave.clicked.connect(lambda: self.clientSave())
        self.ui.buttonClientClear.clicked.connect(lambda: self.clientClear())
        self.ui.buttonServerClear.clicked.connect(lambda: self.serverClear())
        self.ui.buttonClientSend.clicked.connect(
            lambda: self.clientSendMessage())

        self.ui.buttonServerListen.clicked.connect(lambda: self.serverStart())

        self.ui.actionExitApp.triggered.connect(lambda: self.close())

        self.ui.actionClientShowHistory.setChecked(config.clientHistory)
        self.ui.actionClientShowHistory.triggered.connect(lambda: self.showHistory(
            self.ui.clientDockWidget, self.ui.actionClientShowHistory))

        self.ui.actionServerShowHistory.setChecked(config.serverHistory)
        self.ui.actionServerShowHistory.triggered.connect(lambda: self.showHistory(
            self.ui.serverDockWidget, self.ui.actionServerShowHistory))

        self.ui.actionWrapMode.triggered.connect(
            lambda: self.wrapModeChanged())
        self.ui.actionWrapMode.setChecked(config.wrapMode)
        self.wrapModeChanged()

        self.ui.actionDarkStyle.triggered.connect(
            lambda: self.setStyle('dark'))
        self.ui.actionLightStyle.triggered.connect(
            lambda: self.setStyle('light'))

        self.ui.actionSaveConfig.triggered.connect(lambda: self.configSave())
        self.ui.actionHelpAbout.triggered.connect(lambda: self.msgAbout())

        self.ui.radioBtServerGroup.idClicked.connect(lambda: self.serverAck())

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
        self.loadStyle()

    # Root Events
    def resizeEvent(self, event) -> None:
        # print(self.rect().height())
        width = self.rect().width()
        if width < 880:
            if not self.ui.clientDockWidget.isHidden():
                self.ui.clientDockWidget.setHidden(True)
            if not self.ui.serverDockWidget.isHidden():
                self.ui.serverDockWidget.setHidden(True)
        else:
            if self.ui.actionClientShowHistory.isChecked():
                self.ui.clientDockWidget.setHidden(False)
            if self.ui.actionServerShowHistory.isChecked():
                self.ui.serverDockWidget.setHidden(False)

    def popupClientAddresses(self, event):
        index = self.ui.cboxClientHosts.currentIndex()
        if index != -1:
            self.ui.menuCboxClientHosts.popup(QCursor.pos())

    def editorClientHost(self, host, port):
        index = self.ui.cboxClientHosts.currentIndex()
        _host = self.ui.cboxClientHosts.itemText(index)
        if host in self.client_address.keys():
            if host != _host:
                return
            if self.client_address[host] == port:
                return
            status = "changed"
        else:
            self.ui.cboxClientHosts.addItem(host)
            status = "added"
        self.client_address[host] = port
        self.ui.statusBar.showMessage(f"Address '{host}:{port}' {status}!", 5000)

    def deleteClientHost(self):
        index = self.ui.cboxClientHosts.currentIndex()
        if index != -1:
            host = self.ui.cboxClientHosts.itemText(index)
            self.ui.cboxClientHosts.removeItem(index)
            self.client_address.pop(host)
            self.ui.statusBar.showMessage(f"Host '{host}' deleted!", 5000)

    def closeEvent(self, event) -> None:
        self.ui.settingsWindow.setValue('height', self.rect().height())
        self.ui.settingsWindow.setValue('width', self.rect().width())
        self.configSave()

    def loadStyle(self):
        match config.style:
            case 'dark':
                self.ui.actionDarkStyle.trigger()
            case 'light':
                self.ui.actionLightStyle.trigger()

    def setStyle(self, style):
        stylesheet = resourcePath(f'styles\\{style}.qss')
        with open(stylesheet, 'r') as ss:
            self.setStyleSheet(ss.read())
            # self.setStyleSheet('color: red;')
            self.styleApp = style

    def cursorPosition(self):
        position = self.ui.editorClientOutMessage.textCursor().positionInBlock(
        )
        # block = self.ui.editorClientOutMessage.textCursor().blockNumber()
        text = self.ui.editorClientOutMessage.textCursor().block().text()
        segment = text.split('|')
        lenght = 0
        for i in range(len(segment)):
            lenght += len(segment[i]) + 1
            if lenght > position:
                if i == 0:
                    self.ui.labelClientSendInfo.setText(
                        f"Segment: {segment[0]}")
                    break
                element = segment[i]
                if segment[0] == 'MSH':
                    i += 1
                self.ui.labelClientSendInfo.setText(
                    f"{segment[0]}_{i}: '{element}'")
                break

    # messagebox
    def msgAbout(self):
        self.ui.msgBox.setText("<font size='3'>\
                <p>HL7 client and server</p>\
                    <p>Repository: <a style='color:red; font-weight:bold;'\
                        href='https://github.com/TryExceptFinnaly/HL7server-client'>GitHub</a></p>\
                    <p><a style='color:red; font-weight:bold;'\
                        href='https://github.com/TryExceptFinnaly/HL7server-client/raw/master/dist/HL7.exe'>Download</a> current version</p>"
                               )
        self.ui.msgBox.setWindowTitle('HL7 CS')
        self.ui.msgBox.exec()

    # showHistory
    def showHistory(self, dockHistory, actionHistory):
        checked = actionHistory.isChecked()
        if checked and (self.rect().width() < 880):
            self.resize(880, self.rect().height())
        dockHistory.setHidden(not checked)

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
        # if enabled:
        #     self.ui.editorClientOutMessage.setStyleSheet(
        #         'QPlainTextEdit { color: black; }')
        # else:
        #     self.ui.editorClientOutMessage.setStyleSheet(
        #         'QPlainTextEdit { color: gray; }')

    # Result clicked item history
    def resultItemMessages(self, inMsg, outMsg, data):
        inMsg.setPlainText(data.inMsg)
        outMsg.setPlainText(data.outMsg)
        if data.sendInfo:
            self.ui.labelClientSendInfo.setText(data.sendInfo)

    def client_set_port_by_host(self):
        index = self.ui.cboxClientHosts.currentIndex()
        if index != -1:
            host = self.ui.cboxClientHosts.itemText(index)
            if host in self.client_address.keys():
                self.ui.inputClientPort.setText(self.client_address[host])
            else:
                print("Incorrect HOST!")

    def clearItems(self, listHistory, buttonHistory):
        listHistory.clear()
        buttonHistory.setEnabled(False)
        self.ui.statusBar.showMessage('History clear', 5000)

    def configSave(self):
        config.clientAddresses = ""
        for host, port in self.client_address.items():
            config.clientAddresses += f"{host}:{port},"
        config.clientLastAddress = self.ui.cboxClientHosts.currentIndex()
        config.clientTimeOut = self.ui.inputClientTimeout.text()
        config.clientSpam = self.ui.checkClientSpam.isChecked()
        config.clientCountSpam = self.ui.inputClientCountSpam.text()
        config.clientRandom = self.ui.checkClientRandom.isChecked()
        config.clientAN = self.ui.checkClientAccNumber.isChecked()
        config.clientCurrentTime = self.ui.checkClientCurrentTime.isChecked()
        config.clientHistory = self.ui.actionClientShowHistory.isChecked()
        config.serverPort = self.ui.inputServerPort.text()
        config.serverHistory = self.ui.actionServerShowHistory.isChecked()
        config.loadDir = self.loadDir
        config.saveDir = self.saveDir
        config.style = self.styleApp
        config.save()
        print('[CONFIG]: Config saved')

    def loadFile(self):
        try:
            with open(self.loadDir, encoding=client.code, mode='r') as f:
                data = f.read()
                self.ui.editorClientOutMessage.setPlainText(data)
                self.ui.statusBar.showMessage(
                    f'File: "{self.loadDir}" loaded.')
        except Exception as exp:
            print(exp)

    def clientLoad(self):
        file = QFileDialog.getOpenFileName(self, 'Load HL7 message',
                                           self.loadDir,
                                           'HL7 files (*.txt *.hl7)')[0]
        if not file:
            return
        self.loadDir = file
        self.loadFile()

    def saveFile(self):
        try:
            with open(self.saveDir, encoding=client.code, mode='w') as f:
                data = self.ui.editorClientOutMessage.toPlainText()
                f.write(data)
                self.ui.statusBar.showMessage(f'File: "{self.saveDir}" saved.')
        except Exception as exp:
            print(exp)

    def clientSave(self):
        file = QFileDialog.getSaveFileName(self, 'Save HL7 message',
                                           self.saveDir,
                                           'HL7 files (*.txt *.hl7)')[0]
        if not file:
            return
        self.saveDir = file
        self.saveFile()

    def clientClear(self):
        self.ui.editorClientInMessage.setPlainText('')
        self.ui.editorClientOutMessage.setPlainText('')
        self.ui.labelClientSendInfo.setText('')
        self.ui.statusBar.showMessage('Clear', 5000)

    def serverClear(self):
        self.ui.editorServerInMessage.setPlainText('')
        self.ui.editorServerOutMessage.setPlainText('')
        self.ui.statusBar.showMessage('Clear', 5000)

    def clientSendMessage(self):
        if not client.run:
            if not self.ui.inputClientTimeout.text().isdigit():
                self.ui.statusBar.showMessage('Fill in the timeout!', 5000)
                return
            if not self.ui.inputClientPort.text().isdigit():
                self.ui.statusBar.showMessage('Fill in the port!', 5000)
                return
            client.outMsg = self.ui.editorClientOutMessage.toPlainText()
            client.host = self.ui.cboxClientHosts.currentText()
            client.port = int(self.ui.inputClientPort.text())
            client.timeout = int(self.ui.inputClientTimeout.text())
            client.accNumber = self.ui.checkClientAccNumber.isChecked()
            client.curTime = self.ui.checkClientCurrentTime.isChecked()
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
        return f'Average time received {countMsg} messages: {tAllRecv / countMsg:.5f}'

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

    def serverAck(self):
        ack = self.ui.radioBtServerGroup.checkedButton().text()
        server.ack = f'{ack:.2s}'

    def serverStartListen(self):
        while server.run:
            timeMsg, result = server.listen()
            self.serverThreadListen.signals.result.emit(timeMsg, result)
        return 'Server closed'

    def serverResultListen(self, timeMsg: str, result: str):
        # if not server.inMsg:
        #     self.ui.statusBar.showMessage('Empty message received from client',
        #                                   3000)
        #     return
        self.ui.editorServerInMessage.setPlainText(server.inMsg)
        self.ui.editorServerOutMessage.setPlainText(server.outMsg)
        text = f'[{timeMsg}]: From {result}'
        msg = DataItems(self.ui.editorServerInMessage.toPlainText(),
                        self.ui.editorServerOutMessage.toPlainText(), '')
        msg.setText(text)
        self.ui.listServerHistory.addItem(msg)

    def serverStopListen(self, result: str):
        self.ui.statusBar.showMessage(result, 3000)
        self.ui.buttonServerListen.setText('START SERVER')
        self.ui.editorServerOutMessage.setReadOnly(False)

    def eventFilter(self, source: 'QObject', event: 'QEvent') -> bool:
        if event.type() == QEvent.Type.ContextMenu and (source is self.ui.labelClientSendInfo) and (
                self.ui.labelClientSendInfo.text() != ""):
            if self.ui.menuClipboard.exec(event.globalPos()):
                app.clipboard().setText(self.ui.labelClientSendInfo.text())
            return True
        if event.type() == QEvent.Type.KeyPress and (
                (source is self.ui.cboxClientHosts) or (source is self.ui.inputClientPort)):
            key = event.key()
            host = self.ui.cboxClientHosts.currentText()
            port = self.ui.inputClientPort.text()
            if ((key == Qt.Key.Key_Return) or (key == Qt.Key.Key_Enter)) and host != "" and port != "":

                self.editorClientHost(host, port)
        return super().eventFilter(source, event)


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


def resourcePath(relative):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(os.path.abspath("."), relative)


if __name__ == '__main__':
    config = Config('config.ini')
    config.load()

    client = ClientHL7('127.0.0.1', 6005,
                       config.clientTimeOut)
    server = ServerHL7('127.0.0.1', config.serverPort)

    app = QApplication(sys.argv)
    root = MainWindow()
    root.setWindowTitle('HL7 CS v' + app.applicationVersion())
    root.show()

    sys.exit(app.exec())
