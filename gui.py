from PyQt5.QtWidgets import *
import sys

class UI(QMainWindow):
	def __init__(self):
		QWidget.__init__(self)
		self.setFixedHeight(600) # autofit table contents and resize the window
		self.setFixedWidth(800)

		self.setWindowTitle('Network Packet Sniffer')
		self.displayMenu()

		self.table_widget = setTable()
		self.widget = QWidget(self)
		layout = QGridLayout()
		self.widget.setLayout(layout)
		layout.addWidget(self.table_widget)

		self.setCentralWidget(self.widget)


	def displayMenu(self):
		mainMenu = self.menuBar()

		# Menu Items

		fileMenu = mainMenu.addMenu('File')
		fileMenu.addAction('Export to .csv')
		fileMenu.addAction('Import from .csv')
		
		filterMenu = mainMenu.addMenu('Filter')
		aboutMenu = mainMenu.addMenu('About')

		# Buttons

		startbutton = QPushButton('Start Capturing', self)
		startbutton.clicked.connect(self.onClickStart)
		startbutton.setGeometry(150, 0, 120, 25)

		stopbutton = QPushButton('Stop Capturing', self)
		stopbutton.setGeometry(280, 0, 120, 25)
		stopbutton.clicked.connect(self.onClickStop)

		self.show()

	# Button functions

	def onClickStart(self):
		pass

	def onClickStop(self):
		pass

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
		self.tableWidget = QTableWidget()
		self.tableWidget.setRowCount(10)
		self.tableWidget.setColumnCount(5)
		self.tableWidget.setHorizontalHeaderLabels(['Protocol', 'Source IP', 'Destination IP', 'Source Port', 'Destination port'])
		
		self.tableWidget.setItem(0,0, QTableWidgetItem('test'))  # get items dynamically (functions.py)
		self.tableWidget.resizeColumnsToContents()


def main():
	app = QApplication(sys.argv)
	window = UI()
	window.show()

	sys.exit(app.exec_())


main()