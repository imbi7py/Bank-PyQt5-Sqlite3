from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from enum import Enum
import db
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox

class TransfersW(QtWidgets.QMainWindow):
	class CMBBOX_TYPE_INPUT_STATE(Enum):
		ID = 1
		PHONE = 2

	def __init__(self, user_data):
		self.user_data = user_data
		super().__init__(None, Qt.WindowFlags())
		self.init_window()
		self.LBL_USERNAME_START_TEXT   = self.window.lbl_username.text()
		self.LBL_PHONE_USER_START_TEXT = self.window.lbl_phone_user.text()
		self.LBL_COMMISSION_START_TEXT = self.window.lbl_commission.text()
		self.LBL_PAYID_START_TEXT	   = self.window.lbl_payid.text()
		self.LBL_EMAIL_STARR_TEXT	   = self.window.lbl_email.text()

	def init_window(self):
		self.window = uic.loadUi("ui\\transfersw.ui")
		self.window.show()
		self.window.cmbbox_type_input.currentTextChanged.connect(
										self.cmbbox_type_input_changed)
		self.cmbbox_type_input_changed()
		self.window.le_user.textChanged.connect(self.input_username)
		self.window.le_count.textChanged.connect(self.input_count)
		self.window.btn_transfer.clicked.connect(self.transfer)

	def input_username(self):
		cmbbox_state = self.cmmbox_type_input_state()
		if cmbbox_state == self.CMBBOX_TYPE_INPUT_STATE.ID:
			field = "id"
		elif cmbbox_state == self.CMBBOX_TYPE_INPUT_STATE.PHONE:
			field = "phone_number"
		userdata_list = db.read_table_column(db.TB_USERDATA, field)
		le_user_input = self.window.le_user.text()
#		print("le_user_input:", le_user_input)
#		print("userdata_list:", userdata_list)
		lbl_username_text	= self.LBL_USERNAME_START_TEXT
		lbl_phone_user_text	= self.LBL_PHONE_USER_START_TEXT
		lbl_email_text		= self.LBL_EMAIL_STARR_TEXT
		if field == "id":
			try:
				le_user_input = int(le_user_input)
			except:
				pass
		if le_user_input in userdata_list:
			row_data = db.read_table_row_by_field(db.TB_USERDATA,
												  field,
												  le_user_input)
#			print(row_data)
			lbl_username_text	+= ' ' + row_data["username"]
			lbl_phone_user_text	+= ' ' + row_data["phone_number"]
			lbl_email_text		+= ' ' + row_data["email_address"]
		else:
			pass
		self.window.lbl_username.setText(lbl_username_text)
		self.window.lbl_phone_user.setText(lbl_phone_user_text)
		self.window.lbl_email.setText(lbl_email_text)

	def input_count(self):
		le_count_input = self.window.le_count.text()
		lbl_commission_text	= self.LBL_COMMISSION_START_TEXT
		if le_count_input != "":
			lbl_commission_text += ' ' + '0'
		self.window.lbl_commission.setText(lbl_commission_text)

	def cmbbox_type_input_changed(self):
		cmbbox_state = self.cmmbox_type_input_state()
		if cmbbox_state == self.CMBBOX_TYPE_INPUT_STATE.ID:
			le_placeholder_text = "Введите id пользователя:"
		elif cmbbox_state == self.CMBBOX_TYPE_INPUT_STATE.PHONE:
			le_placeholder_text = "Введите номер телефона пользователя:"
		self.window.le_user.setPlaceholderText(le_placeholder_text)

	def cmmbox_type_input_state(self):
		text = self.window.cmbbox_type_input.currentText()
		if text == "Перевод по id пользователя":
			return self.CMBBOX_TYPE_INPUT_STATE.ID
		elif text == "Перевод по номеру телефона":
			return self.CMBBOX_TYPE_INPUT_STATE.PHONE
		return None

	def transfer(self):
		def is_number(s):
			try:
				float(s)
				return True
			except ValueError:
				return False
		le_user_input  = self.window.le_user.text()
		le_count_input = self.window.le_count.text()
		le_msg_input   = self.window.le_msg.text()

		if is_number(le_count_input) == False:
			print("Введено не число")
			return

		sender_id = self.user_data["id"]
		cmbbox_state = self.cmmbox_type_input_state()
		if cmbbox_state == self.CMBBOX_TYPE_INPUT_STATE.ID:
			try:
				receiver_id = int(le_user_input)
			except:
				return
		elif cmbbox_state == self.CMBBOX_TYPE_INPUT_STATE.PHONE:
			userdata_list = db.read_table_column(db.TB_USERDATA, "phone_number")
			if le_user_input in userdata_list:
				row_data = db.read_table_row_by_field(db.TB_USERDATA,
													  "phone_number",
													  le_user_input)
				receiver_id = row_data["id"]
		if sender_id == receiver_id:
			print("Нельзя отправить деньги самому себе")
			return
		sender_data = db.read_table_row_by_field(db.TB_USERDATA,
												 "id",
												 sender_id)
		receiver_data = db.read_table_row_by_field(db.TB_USERDATA,
												   "id",
												   receiver_id)

		sender_balance_now = sender_data["balance"] - float(le_count_input)
		if sender_balance_now < 0:
			print("Баланс отправителя недостаточен")
			return
		receiver_balance_now = receiver_data["balance"] + float(le_count_input)
		db.replace_table_row_field(table_data=db.TB_USERDATA,
								   row=sender_id,
								   value=sender_balance_now,
								   value_name="balance")

		db.replace_table_row_field(table_data=db.TB_USERDATA,
								   row=receiver_id,
								   value=receiver_balance_now,
								   value_name="balance")

		self.FIELDS_LIST = ["id", "id_sender", "id_receiver", "currency",
					   		"value", "commission", "date", "msg"]
		db.write_table(
			db.TB_TRANSFERDATA,
			sender_id,					#id_sender
			receiver_id,				#id_receiver
			sender_data["currency"],	#currency
			float(le_count_input),		#value
			0.0,						#commission
			datetime.now(),				#date
			le_msg_input				#msg
		)
		reply = QMessageBox.question(self,
									 "Состояние платежа",
									 "Транзакция прошла успешно!",
									 QMessageBox.Ok)
		self.window.hide()