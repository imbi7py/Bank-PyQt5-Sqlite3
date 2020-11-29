from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt

class SettingsW(QtWidgets.QMainWindow):
	def __init__(self, user_data):
		super().__init__(None, Qt.WindowFlags())
		self.window = uic.loadUi("ui\\settingsw.ui")
		self.window.show()