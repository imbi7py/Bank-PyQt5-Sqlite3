from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
import json
import sys
import os
from registrate import Registratew
from pswdforget import Pswd_forgetw
from main import MainW
import config
import db
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
	"lbl_input": {
		"basic": """
				color: #000000;
			""",
		"error": """
				color: #883333;
			"""
	}
}

loginw = None
class Loginw(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__(None, Qt.WindowFlags())
		self.window = uic.loadUi("ui\\loginw.ui")
		config.init()
		self.username = config.get_field("current_user")
		if self.username != None:
			self.open_mainw(self.username, self)
			return
		self.init_window()

	def init_window(self):
		self.window.show()
		self.window.btn_login.clicked.connect(self.login)
		self.window.btn_pswd_forget.clicked.connect(self.open_pswd_forgetw)
		self.window.btn_to_registration.clicked.connect(self.open_registratew)

	def login(self):
		def set_error(lbl_text, le_username_style, le_pswd_style):
			self.window.lbl_input.setText(lbl_text)
			self.window.le_username.setStyleSheet(le_username_style)
			self.window.le_pswd.setStyleSheet(le_pswd_style)
			self.window.lbl_input.setStyleSheet(STYLE["lbl_input"]["error"])

		username = self.window.le_username.text()
		password = self.window.le_pswd.text()
		if (len(username) <= 0) & (len(password) <= 0):
			set_error(lbl_text="Имя пользователя и пароль не введены",
					  le_username_style=STYLE["le"]["error"],
					  le_pswd_style=STYLE["le"]["error"])
			return
		if (len(username) <= 0):
			set_error(lbl_text="Имя пользователя не введено",
					  le_username_style=STYLE["le"]["error"],
					  le_pswd_style=STYLE["le"]["basic"])
			return
		if (len(password) <= 0):
			set_error(lbl_text="Пароль не введен",
					  le_username_style=STYLE["le"]["basic"],
					  le_pswd_style=STYLE["le"]["error"])
			return
		userdata_list = db.read_table(db.TB_USERDATA)
		user_exist = False
		for row in userdata_list:
			if username == row[1]:
				user_exist = row
				break
		if user_exist == False:
			set_error(lbl_text="Пользователь не найден",
					  le_username_style=STYLE["le"]["error"],
					  le_pswd_style=STYLE["le"]["basic"])
			return
	#find index of le_username in username_list. If exist compare passwords
		if make_hash(username, password) == row[2]:
			if self.window.chkbox_remember.isChecked():
				config.set_field("current_user", username)
			print("Авторизация успешна. Здравствуй,", username)
			self.open_mainw(username, self)
			return
		set_error(lbl_text="Пароль введен неверно",
				  le_username_style=STYLE["le"]["basic"],
				  le_pswd_style=STYLE["le"]["error"])

	def open_mainw(self, username, loginw):
		self.window.hide()
		try:
			self.registratew.window.hide()
		except:
			pass
		try:
			self.pswdforget.window.hide()
		except:
			pass
		user_data = db.read_table_get_dict_by_field(db.TB_USERDATA,
													"username",
													username)
		self.mainw = MainW(user_data, self)
		self.mainw.window.show()

	def open_registratew(self):
		self.registratew = Registratew(self)
		self.registratew.window.show()

	def open_pswd_forgetw(self):
		self.pswd_forgetw = Pswd_forgetw()
		self.pswd_forgetw.window.show()

if __name__ == "__main__":
	QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
	app = QtWidgets.QApplication([])
	loginw = Loginw()
	sys.exit(app.exec())