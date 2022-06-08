from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt
import sys
import networkProcesses
import csv

info = []


class UI(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)
        UI.listWiget = QListWidget()
        self.setMinimumHeight(600)
        self.setMinimumWidth(800)

        # think of a better name
        self.setWindowTitle("Sniff")
        self.displayMenu()

        self.table_widget = setTable()
        self.widget = QWidget(self)
        layout = QGridLayout()
        self.widget.setLayout(layout)
        layout.addWidget(self.table_widget)

        self.setCentralWidget(self.widget)
        self.scan = False

        self.thread = QThread()
        self.worker = networkProcesses.NetworkProcessWorker()

        # Dock widget to display data
        self.createDockWidget()
        self.show()

    def createDockWidget(self):
        self.dock = QDockWidget("Information", self)
        # self.listWiget = QListWidget()
        self.dock.setWidget(self.listWiget)
        # self.dock.setStyleSheet()
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock)

    def updateDock(self):
        print(info)
        self.listWiget.clear()
        self.listWiget.addItems(
            [
                "Protocol ",
                info[0],
                "------------",
                "Source IP",
                info[1],
                "------------",
                "Destination IP",
                info[2],
                "------------",
                "Source Port",
                info[3],
                "------------",
                "Destination port",
                info[4],
                "------------",
                "Data",
                info[5],
            ]
        )

    def exportCall(self):
        print("export clicked")

        # get absolute file name from dialog
        fileName = QFileDialog.getSaveFileName(filter="CSV(*.csv)")
        if fileName[0] == "":
            return
        fileName = fileName[0] + ".csv"
        print(fileName)

        # get table contents
        tableContents = []
        for rowNo in range(self.table_widget.tableWidget.rowCount()):
            row = []
            for colNo in range(self.table_widget.tableWidget.columnCount()):
                # print(self.table_widget.tableWidget.item(colNo,rowNo).text())
                item = self.table_widget.tableWidget.item(rowNo, colNo)
                if item:
                    item = item.text()
                # row.append(self.table_widget.tableWidget.item(rowNo,colNo).text())
                row.append(item)
                print(item)
            # print(row)
            tableContents.append(row)

        # save it to csv at filename
        fields = [
            "Protocol",
            "Source IP",
            "Destination IP",
            "Source Port",
            "Destination Port",
            "Data",
        ]
        with open(fileName, "w") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            csvwriter.writerows(tableContents)

    def importCall(self):
        print("import clicked")
        fileName = QFileDialog.getOpenFileName(filter="CSV(*.csv)")
        if fileName[0] == "":
            return
        fileName = fileName[0]
        print(fileName)

        self.table_widget.tableWidget.clearContents()
        self.table_widget.tableWidget.setRowCount(0)
        with open(fileName, mode="r") as file:
            csvfile = csv.reader(file)
            count = 0
            for line in csvfile:
                if count == 0:
                    pass
                else:
                    print(line)
                    self.table_widget.updateTable(line)
                count += 1

    def displayMenu(self):
        mainMenu = self.menuBar()

        # defining actions
        exportAction = QAction("Export to .csv", self)
        exportAction.triggered.connect(self.exportCall)
        importAction = QAction("Import from .csv", self)
        importAction.triggered.connect(self.importCall)

        # Menu Items

        fileMenu = mainMenu.addMenu("File")
        # fileMenu.addAction('Export to .csv')
        fileMenu.addAction(exportAction)
        fileMenu.addAction(importAction)

        filterMenu = mainMenu.addMenu("Filter")
        aboutMenu = mainMenu.addMenu("About")

        # Buttons

        self.startbutton = QPushButton("Start Capturing", self)
        # self.startbutton.setStyleSheet() -> set icon and colour
        self.startbutton.clicked.connect(self.onClickStart)
        self.startbutton.setGeometry(150, 0, 120, 20)

        self.show()

    def runNetworkProcess(self):
        # moves the worker class to the thread

        self.startbutton.setText("Stop Capturing")
        # self.startbutton.setStyleSheet() -> set icon and colour

        self.threads = []
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.packet.connect(self.table_widget.updateTable)
        self.threads.append(self.worker)
        self.worker.start()

    # Button functions

    def onClickStart(self):
        # adds a new row to the table on click of the button
        networkProcesses.isRun
        if self.startbutton.text() == "Start Capturing":
            print("yes")
            networkProcesses.isRun = True
            self.runNetworkProcess()

        else:
            networkProcesses.isRun = False
            print("Done!")

            self.startbutton.setText("Start Capturing")


# Generate Table


class setTable(QWidget):
    def __init__(self):
        super(setTable, self).__init__()
        self.tableInterface()

    def tableInterface(self):
        self.fetchTable()
        self.layout = QVBoxLayout()
        self.search = QLineEdit(self)
        self.search.setPlaceholderText("Search...")
        self.layout.addWidget(self.search)
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        self.show()
        self.search.textChanged.connect(self.searchItem)

    def fetchTable(self):
        # make a table with headers
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(
            [
                "Protocol",
                "Source IP",
                "Destination IP",
                "Source Port",
                "Destination port",
                "Data",
            ]
        )

        # self.tableWidget.setItem(0,0, QTableWidgetItem('test'))  # get items dynamically (functions.py)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.cellClicked.connect(self.cellClick)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

    def updateTable(self, row):
        # add a row to the end of the table
        print(
            "________________________updating table_________________________________________"
        )
        rowPos = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPos)
        # self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
        itemCount = 0
        for item in row:
            widgetItem = QTableWidgetItem(str(row[itemCount]))
            self.tableWidget.setItem(rowPos, itemCount, widgetItem)
            # self.tableWidget.setItem(rowPos,itemCount, QTableWidgetItem("test"))
            self.tableWidget.scrollToItem(widgetItem)
            print(f"inserted into table ------------{row[itemCount]}-------------")
            itemCount += 1

    # gets cell's contents

    def cellClick(self):
        global info
        info = []
        for self.curr in self.tableWidget.selectedItems():
            # print(self.curr.row(), self.curr.column(), self.curr.text())
            for i in range(6):
                # print(self.tableWidget.item(self.curr.row(), i).text())
                if self.tableWidget.item(self.curr.row(), i):
                    info.append(self.tableWidget.item(self.curr.row(), i).text())
            # print(info)
            UI.updateDock(UI)

    def searchItem(self):
        query = self.search.text()
        for i in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(i, 0)
            self.tableWidget.setRowHidden(i, query not in item.text())


def main():
    app = QApplication(sys.argv)
    window = UI()
    window.show()
    sys.exit(app.exec_())


main()
