from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from datetime import datetime
import db
import os
from hash import make_hash

STYLE = {
	"le": {
		"basic": """
			QLineEdit {
				background: #E0E0E0;
				border: 2px solid #666666;
				border-bottom-width: 1px;
				border-right-width: 1px;
				border-bottom-color: #F9F9F9;
				border-right-color: #F9F9F9;
				color: #000000;
			}""",
		"error": """
			QLineEdit {
				background: #E0E0E0;
				border: 2px solid #CA6666;
				border-bottom-width: 1px;
				border-right-width: 1px;
				border-bottom-color: #AA3333;
				border-right-color: #AA3333;
				color: #000000;
			}"""
	},
	"lbl_info": {
		"basic": """
				color: #000000;
			""",
		"error": """
				color: #883333;
			"""
	},
	"cmbbox": {
		"basic": """
			QComboBox {
				background: #E0E0E0;
				border: 2px solid #666666;
				border-bottom-width: 1px;
				border-right-width: 1px;
				border-bottom-color: #F9F9F9;
				border-right-color: #F9F9F9;
				color: #000000;
			}""",
		"error": """
			QComboBox {
				background: #E0E0E0;
				border: 2px solid #CA6666;
				border-bottom-width: 1px;
				border-right-width: 1px;
				border-bottom-color: #AA3333;
				border-bottom-color: #AA3333;
				color: #000000;
			}"""
	}
}

class Registratew(QtWidgets.QMainWindow):
	def __init__(self, loginw):
		super().__init__(None, Qt.WindowFlags())
		self.loginw = loginw
		self.window = uic.loadUi("ui\\registratew.ui")
		self.window.btn_registration.clicked.connect(self.registrate)
		self.window.show()

	def registrate(self):
		le_list = [{"le": self.window.le_username,
				   "err_msg": "Имя пользователя не введено"},
				   {"le": self.window.le_pswd,
				   "err_msg": "Пароль не введен"},
				   {"le": self.window.le_pswd_rep,
				   "err_msg": "Повтор пароля не введен"},
				   {"le": self.window.le_control_question,
				   "err_msg": "Не введен ответ на контрольный вопрос"},
				   {"le": self.window.le_phone_number,
				   "err_msg": "Не введен номер телефона"},
				   {"le": self.window.le_email,
				   "err_msg": "Не введен адрес электронной почты"}
		]
		if_error = False
		for i in le_list:
			if len(i["le"].text()) == 0:
				print(i["err_msg"])
				i["le"].setStyleSheet(STYLE["le"]["error"])
				if_error = True
			else:
				i["le"].setStyleSheet(STYLE["le"]["basic"])
		if if_error:
			return
		username = self.window.le_username.text()
		password = self.window.le_pswd.text()
		repeat_password = self.window.le_pswd_rep.text()
		control_question_answer = self.window.le_control_question.text()
		phone_number = self.window.le_phone_number.text()
		email = self.window.le_email.text()
		currency = self.window.cmbbox_currency.currentText()
		control_question = self.window.cmbbox_control_question.currentText()
		sex = self.window.cmbbox_sex.currentText()
		balance = 0.0
		if password != repeat_password:
			print("Пароли не совпадают")
			self.window.le_pswd.setStyleSheet(STYLE["le"]["error"])
			self.window.le_pswd_rep.setStyleSheet(STYLE["le"]["error"])

		username_list = db.read_table_column(db.TB_USERDATA, "username")
		if (username in username_list):
			self.window.le_username.setStyleSheet(STYLE["le"]["error"])
			print("Это имя пользователя уже используется")
			return
		email_list = db.read_table_column(db.TB_USERDATA, "email_address")
		if (email in email_list):
			self.window.le_email.setStyleSheet(STYLE["le"]["error"])
			print("Этот email адрес уже используется")
			return
		phone_list = db.read_table_column(db.TB_USERDATA, "phone_number")
		if (phone_number in phone_list):
			self.window.le_phone_numbers.setStyleSheet(STYLE["le"]["error"])
			print("Этот номер телефона уже используется")
			return
		db.write_table(
			db.TB_USERDATA,
			username,				#username
			make_hash(username, password),	#password
			currency,				#currency
			control_question,		#control_question
			control_question_answer,#control_question_answer
			f"user_data{os.path.sep}default{os.path.sep}default.jpg",#avatar_path
			phone_number,	#phone_number
			sex,			#sex
			email,			#email_address
			False,			#email_valid
			datetime.now(),	#reg_date
			0.0				#balance
			)
		os.mkdir(f"user_data{os.path.sep}{username}")
		reply = QMessageBox.question(self,
									 "Подтверждение",
									 "Регистрация прошла успешно!",
									 QMessageBox.Ok)
		self.window.hide()
		self.loginw.init_window()