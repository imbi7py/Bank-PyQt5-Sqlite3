from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from enum import Enum
import db
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from transact_info import Transact_infow


class HistoryW(QtWidgets.QMainWindow):
	class CMBBOX_TYPE_STATE(Enum):
		RECEIVED = 1
		SEND	 = 2
		ALL		 = 3

	def __init__(self, user_data):
		self.user_data = user_data
		super().__init__(None, Qt.WindowFlags())
		self.init_window()

	def init_window(self):
		self.window = uic.loadUi("ui\\historyw.ui")
		self.window.show()
		self.window.cmbbox_type.currentTextChanged.connect(self.init_table)
		self.window.table.cellDoubleClicked.connect(self.doubleclick_item_table)
		self.init_table()

	def init_table(self):
		transfer_data = []
		transfer_tb_data = db.read_table_get_dict(db.TB_TRANSFERDATA)
		if self.cmbbox_type_state() == self.CMBBOX_TYPE_STATE.RECEIVED:
			for i in transfer_tb_data:
				if i["id_receiver"] == self.user_data["id"]:
					transfer_data.append(i)
		elif self.cmbbox_type_state() == self.CMBBOX_TYPE_STATE.SEND:
			for i in transfer_tb_data:
				if i["id_sender"] == self.user_data["id"]:
					transfer_data.append(i)
		elif self.cmbbox_type_state() == self.CMBBOX_TYPE_STATE.ALL:
			for i in transfer_tb_data:
				if (i["id_receiver"] == self.user_data["id"]) |\
				   (i["id_sender"] == self.user_data["id"]):
					transfer_data.append(i)
		#print(transfer_data)
		self.window.table.clearContents()
		self.window.table.setRowCount(len(transfer_data))
		def add_item_tb(tb, row, column, _str):
			tb.setItem(row, column, QTableWidgetItem(_str))

		for i in range(len(transfer_data)):
			sender_data = db.read_table_row_by_field(
											db.TB_USERDATA,
											"id",
											transfer_data[i]["id_sender"])
			add_item_tb(self.window.table, i, 0, sender_data["username"])
			add_item_tb(self.window.table, i, 1, str(transfer_data[i]["value"]))
			add_item_tb(self.window.table, i, 2, str(transfer_data[i]["commission"]))
			add_item_tb(self.window.table, i, 3, str(transfer_data[i]["date"]))
			add_item_tb(self.window.table, i, 4, str(transfer_data[i]["id"]))
		self.transfer_data = transfer_data

	def doubleclick_item_table(self, row):
		self.transact_infow = Transact_infow(self.transfer_data[row])

	def cmbbox_type_state(self):
		text = self.window.cmbbox_type.currentText()
		if text == "Входящие":
			return self.CMBBOX_TYPE_STATE.RECEIVED
		elif text == "Исходящие":
			return self.CMBBOX_TYPE_STATE.SEND
		elif text == "Все":
			return self.CMBBOX_TYPE_STATE.ALL
		return None