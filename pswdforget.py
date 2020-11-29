from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
import db

class Pswd_forgetw(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__(None, Qt.WindowFlags())
		self.window = uic.loadUi("ui\\pswd_forgetw.ui")
		self.window.btn_restore.clicked.connect(self.restore_password)
		self.init_window()
		
	def init_window(self):
		self.window.show()
		self.window.le_username.textChanged.connect(self.input_username)

	def input_username(self, le_text):
		userdata_list = db.read_table(db.TB_USERDATA)
		row = None
		for i in userdata_list:
			if le_text == i[1]: #1 = username
				row = i
				break
		if row == None:
			self.window.lbl_control_question2.setText("")
			return
		self.window.lbl_control_question2.setText(row[4]) #4 = control_question

	def restore_password(self):
		username = self.window.le_username.text()
		control_question_answer = self.window.le_control_question.text()
		userdata_list = db.read_table(db.TB_USERDATA)
		row = None
		for i in userdata_list:
			if username == i[1]: #1 = username
				row = i
				break
		if row == None:
			self.window.lbl_pswd.setText("Пользователь не найден")
			return
		if row[5] == control_question_answer:
			self.window.lbl_pswd.setText(f"Пароль: {row[2]}") #2 = pswd
		else:
			self.window.lbl_pswd.setText("Неверный ответ на контрольный вопрос")