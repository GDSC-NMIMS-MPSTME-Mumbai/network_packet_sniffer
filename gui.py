from re import U
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt
import sys
import networkProcesses
info = []

class UI(QMainWindow):
	def __init__(self):
		QWidget.__init__(self)
		UI.listWiget = QListWidget()
		self.setMinimumHeight(600)
		self.setMinimumWidth(800)

		self.setWindowTitle('Network Packet Sniffer')
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
		self.dock = QDockWidget("Data", self)
		# self.listWiget = QListWidget()
		self.dock.setWidget(self.listWiget)
		# self.listWiget.addItems(['test'])
		# self.dock.setStyleSheet()
		self.addDockWidget(Qt.BottomDockWidgetArea, self.dock)

	def updateDock(self):
		print(info)
		# UI.listWiget = QListWidget()
		self.listWiget.clear()
		self.listWiget.addItems(['Protocol ', info[0], '------------','Source IP', info[1], '------------',  'Destination IP', info[2], '------------',  'Source Port', info[3], '------------',  'Destination port', info[4], '------------',  'Data', info[5]])
		# pass
		

	def displayMenu(self):
		mainMenu = self.menuBar()

		# Menu Items

		fileMenu = mainMenu.addMenu('File')
		fileMenu.addAction('Export to .csv')
		fileMenu.addAction('Import from .csv')
		
		filterMenu = mainMenu.addMenu('Filter')
		aboutMenu = mainMenu.addMenu('About')

		# Buttons

		self.startbutton = QPushButton('Start Capturing', self)
		self.startbutton.clicked.connect(self.onClickStart)
		self.startbutton.setGeometry(150, 0, 120, 25)

		self.show()

	def runNetworkProcess(self):
		# self.thread = QThread()
		# self.worker = networkProcess.NetworkProcessWorker()
		
		# moves the worker class to the thread
		self.startbutton.setText('Stop Capturing')
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
		if self.startbutton.text() == 'Start Capturing':
			print('yes')
			networkProcesses.isRun = True
			self.runNetworkProcess()
		
		else:
			networkProcesses.isRun = False
			print('Done!')

			self.startbutton.setText('Start Capturing')

# Generate Table

class setTable(QWidget):
	def __init__(self):
		super(setTable, self).__init__()
		self.tableInterface()

	def tableInterface(self):
		self.fetchTable()
		self.layout = QVBoxLayout()
		self.layout.addWidget(self.tableWidget)
		self.setLayout(self.layout)

		self.show()

	def fetchTable(self):
		# make a table with headers
		self.tableWidget = QTableWidget()
		self.tableWidget.setRowCount(0)
		self.tableWidget.horizontalHeader().setStretchLastSection(True)

		self.tableWidget.setColumnCount(6)
		self.tableWidget.setHorizontalHeaderLabels(['Protocol', 'Source IP', 'Destination IP', 'Source Port', 'Destination port', 'Data'])
		
		# self.tableWidget.setItem(0,0, QTableWidgetItem('test'))  # get items dynamically (functions.py)
		self.tableWidget.resizeColumnsToContents()
		self.tableWidget.cellClicked.connect(self.cellClick)
	def updateTable(self,row):
		# add a row to the end of the table
		print("________________________updating table_________________________________________-")
		rowPos = self.tableWidget.rowCount()
		self.tableWidget.insertRow(rowPos)
		# self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
		itemCount = 0
		for item in row:
			self.tableWidget.setItem(rowPos,itemCount, QTableWidgetItem(str(row[itemCount])))
			# self.tableWidget.setItem(rowPos,itemCount, QTableWidgetItem("test"))
			print(f"inserted into table ------------{row[itemCount]}-------------")
			itemCount+=1


	# gets cell's contents 

	def cellClick(self):
		global info
		info = []
		for self.curr in self.tableWidget.selectedItems():
			# print(self.curr.row(), self.curr.column(), self.curr.text())
			for i in range(6):
				# print(self.tableWidget.item(self.curr.row(), i).text())
				info.append(self.tableWidget.item(self.curr.row(), i).text())
			# print(info)
			UI.updateDock(UI)
			


def main():
	app = QApplication(sys.argv)
	window = UI()
	window.show()
	

	sys.exit(app.exec_())


main()