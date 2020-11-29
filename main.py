from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from profile import ProfileW
from settings import SettingsW
from transfers import TransfersW
from history import HistoryW
from exchange_rates import Exchange_ratesW
import config

class MainW(QtWidgets.QMainWindow):
	def __init__(self, user_data, loginw):
		self.user_data = user_data
		self.loginw = loginw
		super().__init__(None, Qt.WindowFlags())
		self.init_window()
		self.show_info()

	def init_window(self):
		self.window = uic.loadUi("ui\\mainw.ui")
		self.window.show()
		self.window.btn_to_profile.clicked.connect(self.open_profilew)
		self.window.btn_to_settings.clicked.connect(self.open_settingsw)
		self.window.btn_to_transfers.clicked.connect(self.open_transfersw)
		self.window.btn_to_history.clicked.connect(self.open_historyw)
		self.window.btn_to_exchange_rates.clicked.connect(self.open_exchange_ratesw)
		self.window.btn_to_exit.clicked.connect(self.btn_to_exit)

	def show_info(self):
		id_data = f"Номер банковского счета: {self.user_data['id']}"
		self.window.lbl_id.setText(id_data)
		balance_data = f"На счету: {self.user_data['balance']}"
		self.window.lbl_balance.setText(balance_data)

	def open_profilew(self):
		self.profilew = ProfileW(self.user_data)

	def open_settingsw(self):
		self.settingsw = SettingsW(self.user_data)

	def open_transfersw(self):
		self.transfersw = TransfersW(self.user_data)

	def open_historyw(self):
		self.historyw = HistoryW(self.user_data)

	def open_exchange_ratesw(self):
		self.exchange_ratesw = Exchange_ratesW(self.user_data)

	def btn_to_exit(self):
		reply = QMessageBox.question(self,
									 "Подтверждение",
									 "Вы точно хотите выйти?",
									 QMessageBox.Yes | QMessageBox.No,
									 QMessageBox.No)
		if reply == QMessageBox.Yes:
			self.window.hide()
			try:
				self.settingsw.window.hide()
			except:
				pass
			try:
				self.transfersw.window.hide()
			except:
				pass
			try:
				self.profilew.window.hide()
			except:
				pass
			try:
				self.exchange_ratesw.window.hide()
			except:
				pass
			try:
				self.historyw.window.hide()
			except:
				pass
			self.loginw.init_window()
			config.set_field("current_user", None)