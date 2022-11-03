import sys
import time
import os
import requests
import json

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal

from lib.file_readers import iter_texts, iter_supported_files

# inspiration https://www.saltycrane.com/blog/2007/06/more-pyqt-example-code/

BAR_LENGTH = 100


class CreateEmbeddings(QThread):
    progressSig = pyqtSignal(int)
    completeSig = pyqtSignal(object)

    def __init__(self, dir=""):
        super(QThread, self).__init__()
        self.dir = dir

    def run(self):
        """
        This is very janky because we cant see the length of the texts generator
        Need to fix this
        """
        self.progressSig.emit(0)
        length = len(list(iter_supported_files(self.dir)))
        progressCount = 0
        result = []
        for value in iter_texts(
            self.dir
        ):  # TODO iter_texts should probably take a file iterator as an input so we can avoid calling iter_supported_files twice
            # Better to have separation of concerns anyway.   (I realize I wrote iter_texts lol)
            result.append({"file": value[0], "text": value[1]})
            progressCount += 1
            self.progressSig.emit(int((progressCount / length) * 100))

        self.progressSig.emit(BAR_LENGTH)
        self.completeSig.emit(result)


class HTTPS_Get(QThread):
    completeSig = pyqtSignal(object)

    def __init__(self, url, data):
        super(QThread, self).__init__()
        self.url = url
        self.data = data

    def run(self):
        response = requests.get(self.url, json=self.data)
        print(response)
        self.completeSig.emit(response)


class HTTPS_Post(QThread):
    completeSig = pyqtSignal(object)

    def __init__(self, url, data):
        super(QThread, self).__init__()
        self.url = url
        self.data = data

    def run(self):
        # post the data as a json
        print(self.data)
        response = requests.post(self.url, json=self.data)
        self.completeSig.emit(response)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.title = "Semantic File Search"
        # TODO maybe have this be configurable in a config file... not sure if it really matters though
        self.left = 10
        self.top = 10
        self.width = 640 * 2
        self.height = 640
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.tabsWindow = TabsWindow()

        self.setCentralWidget(self.tabsWindow)
        self.show()


class TabsWindow(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.generate = EmbeddingWidget()
        self.search = SearchWidget()

        # Add tabs
        self.tabs.addTab(self.generate, "Generate Embeddings")
        self.tabs.addTab(self.search, "Search Embeddings")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


# TODO the Embeddings and Search Widgets are big enough they could probably get their own files


class EmbeddingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        layout = QGridLayout()

        self.textWindow = QTextBrowser(self, readOnly=True)
        layout.addWidget(
            self.textWindow, 0, 0, 1, 2
        )  # TODO It's a bit unclear what these numbers mean, perhaps (I realize he said not to put this in the code review) a comment or making the numbers constants would be helpful.

        self.filepathBox = QLineEdit(self, readOnly=True, placeholderText="...")
        layout.addWidget(self.filepathBox, 1, 0)

        self.fileSelectBtn = QPushButton("Select a File")
        self.fileSelectBtn.clicked.connect(self.folderDialog)
        layout.addWidget(self.fileSelectBtn, 1, 1)

        self.serverAddressBox = QLineEdit(self, placeholderText="Server Address")
        self.serverAddressBox.textChanged.connect(self.buttonCheck)
        layout.addWidget(self.serverAddressBox, 2, 0)

        self.runBtn = QPushButton("Collect Text")
        self.runBtn.clicked.connect(self.run)
        self.runBtn.setEnabled(False)
        layout.addWidget(self.runBtn, 2, 1)

        self.saveFileName = QLineEdit(self, placeholderText="Embedding file name")
        self.saveFileName.textChanged.connect(self.buttonCheck)
        layout.addWidget(self.saveFileName, 3, 0)

        self.sendBtn = QPushButton("Send Collected Text")
        self.sendBtn.clicked.connect(self.send)
        self.sendBtn.setEnabled(False)
        layout.addWidget(self.sendBtn, 3, 1)

        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(BAR_LENGTH)
        self.progressBar.hide()
        layout.addWidget(self.progressBar, 4, 0)

        self.setLayout(layout)

    def folderDialog(self):
        options = QFileDialog.Options()
        options |= (
            QFileDialog.Option.ShowDirsOnly
        )  # TODO why is there a bit-wise-or-equals here?
        directory = QFileDialog.getExistingDirectory(
            self, "QFileDialog.getExistingDirectory()", "", options=options
        )
        if directory:
            self.filepathBox.setText(directory)
        self.buttonCheck()

    def run(self):
        self.textWindow.setText(
            "Grabbing text from {}...".format(self.filepathBox.text())
        )

        self.progressBar.show()
        self.calcThread = CreateEmbeddings(
            dir=os.path.normpath(self.filepathBox.text())
        )
        self.calcThread.progressSig.connect(self.progressCountCallback)
        self.calcThread.completeSig.connect(self.completeCallback)
        self.calcThread.start()

    def send(self):
        self.textWindow.setText("Sending to server...")
        self.sendThread = HTTPS_Post(
            "http://24.34.20.62:55889/data_upload/",
            self.scrapedData,  # TODO this could definitely be in a config file <- response: I decided to make the server address a user input
        )
        self.sendThread.completeSig.connect(self.sendCompleteCallback)
        self.sendThread.start()

    def buttonCheck(self):
        if (
            self.filepathBox.text() != ""
            and self.saveFileName.text() != ""
            and self.serverAddressBox.text() != ""
        ):
            self.runBtn.setEnabled(True)
        else:
            self.runBtn.setEnabled(False)

    def progressCountCallback(self, value):
        self.progressBar.setValue(value)

    def completeCallback(self, value):
        displayStr = "Text Found\n\n"
        # Loop over value dict and add file name and text to display string
        for item in value:
            displayStr += "File: {}\n{} \n \n".format(item["file"], item["text"])

        self.textWindow.setText(displayStr)
        self.sendBtn.setEnabled(True)
        self.progressBar.hide()
        self.scrapedData = {"data": value}

    def sendCompleteCallback(self, value):
        # print status code of value which is an http response
        print(value.status_code)
        print(value.text)
        if value.status_code == 200 or value.status_code == 202:
            data = value.json()
            print(data)
            self.textWindow.setText(f'Successfully sent! Batch Id: {data["batch_id"]}')
        else:
            self.textWindow.setText("Error sending!")
        self.sendBtn.setEnabled(False)


class SearchWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        layout.setColumnStretch(0, 1)

        self.textWindow = QTextBrowser(self, readOnly=True)

        layout.addWidget(self.textWindow, 0, 0, 1, 2)

        self.searchField = QLineEdit(self, placeholderText="Search text...")
        self.searchField.textChanged.connect(self.buttonCheck)
        layout.addWidget(self.searchField, 1, 0)

        self.serverAddressBox = QLineEdit(self, placeholderText="Server Address")
        self.serverAddressBox.textChanged.connect(self.buttonCheck)
        layout.addWidget(self.serverAddressBox, 2, 0)

        self.idField = QLineEdit(self, placeholderText="BatchId")
        self.idField.textChanged.connect(self.buttonCheck)
        layout.addWidget(self.idField, 1, 1)

        self.runBtn = QPushButton("Search")
        self.runBtn.clicked.connect(self.run)
        self.runBtn.setEnabled(False)
        layout.addWidget(self.runBtn, 2, 1)

        self.setLayout(layout)

    def buttonCheck(self):
        if (
            self.searchField.text() != ""
            and self.idField.text() != ""
            and self.serverAddressBox.text() != ""
        ):
            self.runBtn.setEnabled(True)
        else:
            self.runBtn.setEnabled(False)

    def run(self):
        # Create a thread to get the data from the server
        self.textWindow.setText("Searching...")
        self.data = {
            "batchId": str(self.idField.text()),
            "query": str(self.searchField.text()),
        }
        print(self.data)
        self.searchThread = HTTPS_Get(
            "http://24.34.20.62:55889/search/", self.data
        )  # TODO also could be loaded form a config file
        self.searchThread.completeSig.connect(self.completeCallback)
        self.searchThread.start()

    def completeCallback(self, value):
        # print status code of value which is an http response
        if value.status_code == 200:
            data = value.json()["data"]
            # unpack json into human readable text
            text = ""
            for i in data:
                text += f'File: {i["filepath"]} \nScore: {i["similarity"]} \nText: {i["text"]}\n\n'
            self.textWindow.setText(text)
            print(text)
        elif value.status_code == 404:
            self.textWindow.setText("No results found for this BatchId!")
        else:
            self.textWindow.setText("Error sending!")


# TODO main could be in a separate file and import what it needs
# TODO main could also be responsible for loading the config file
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    mw = MainWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
