from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QKeySequence, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QInputDialog
import requests
import os
import db

class ProfileW(QtWidgets.QMainWindow):
	def __init__(self, user_data):
		self.user_data = user_data
		super().__init__(None, Qt.WindowFlags())
		self.init_window()

	def init_window(self):
		self.window = uic.loadUi("ui\\profilew.ui")
		self.window.show()
		self.window.avatar.clicked.connect(self.avatar_btn)
		self.window.btn_change_by_url.clicked.connect(self.avatar_change_by_url)
		self.window.btn_change_by_file.clicked.connect(self.avatar_btn)
		self.init_labels()

	def init_labels(self):
		self.window.lbl_id_value.setText(str(self.user_data["id"]))
		self.window.lbl_username_value.setText(str(self.user_data["username"]))
		self.window.lbl_currency_value.setText(str(self.user_data["currency"]))
		self.window.lbl_balance_value.setText(str(self.user_data["balance"]))
		self.window.lbl_email_value.setText(str(self.user_data["email_address"]))
		self.window.lbl_sex_value.setText(str(self.user_data["sex"]))
		self.window.lbl_phone_value.setText(str(self.user_data["phone_number"]))
		self.window.lbl_regdate_value.setText(str(self.user_data["reg_date"]))
		self.set_avatar(self.user_data["avatar_path"])

	def avatar_btn(self):
		fname = QFileDialog.getOpenFileName(self, "Open file", "")[0]
		if fname == "":
			return
		self.set_avatar(fname)
		self.user_data["avatar_path"] = fname
		db.replace_table_row_field(table_data=db.TB_USERDATA,
								   row=self.user_data["id"],
								   value=fname,
								   value_name="avatar_path")

	def avatar_change_by_url(self):
		url, ok = QInputDialog.getText(self,
							"Установить аватар",
							"Введите url-адрес фотографии:")
		if ok:
			r = requests.get(url)
			ext = r.headers["content-type"]
			ext = ext.split('/')[1]
			fname = f"user_data{os.path.sep}{self.user_data['username']}"\
					f"{os.path.sep}avatar.{ext}"
			with open(fname, "wb") as f:
			    f.write(r.content)
			self.set_avatar(fname)
			self.user_data["avatar_path"] = fname
			db.replace_table_row_field(table_data=db.TB_USERDATA,
									   row=self.user_data["id"],
									   value=fname,
									   value_name="avatar_path")

	def set_avatar(self, path_image):
		avatar = QIcon(QPixmap(path_image))
		self.window.avatar.setIcon(avatar)
		self.window.avatar.setIconSize(QSize(self.window.avatar.width() - 4,
											 self.window.avatar.height() - 4))