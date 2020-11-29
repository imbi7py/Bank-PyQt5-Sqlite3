from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QKeySequence, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QInputDialog
import requests
import os
import db

class Transact_infow(QtWidgets.QMainWindow):
	def __init__(self, transact_data):
		self.transact_data = transact_data
		super().__init__(None, Qt.WindowFlags())
		self.init_window()

	def init_window(self):
		self.window = uic.loadUi("ui\\transact_infow.ui")
		self.window.show()
		self.init_labels()

	def init_labels(self):
		sender_data = db.read_table_row_by_field(
										db.TB_USERDATA,
										"id",
										self.transact_data["id_sender"])
		self.window.lbl_transfer_id_value.setText(str(self.transact_data["id"]))
		self.window.lbl_date_value.setText(str(self.transact_data["date"]))
		self.window.lbl_sender_id_value.setText(str(sender_data["id"]))
		self.window.lbl_sender_name_value.setText(str(sender_data["username"]))
		self.window.lbl_sender_phone_value.setText(str(sender_data["phone_number"]))
		self.window.lbl_sender_email_value.setText(str(sender_data["email_address"]))
		self.window.lbl_value_value.setText(str(self.transact_data["value"]))
		self.window.lbl_commission_value.setText(str(self.transact_data["commission"]))
		self.window.lbl_currency_value.setText(str(self.transact_data["currency"]))
		self.window.lbl_msg_value.setText(str(self.transact_data["msg"]))