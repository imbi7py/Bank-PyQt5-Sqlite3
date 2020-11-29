from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import db
import requests
from datetime import datetime

class Exchange_ratesW(QtWidgets.QMainWindow):
	def __init__(self, user_data):
		self.user_data = user_data
		super().__init__(None, Qt.WindowFlags())
		self.init_window()
		self.init_values()

	def init_window(self):
		self.window = uic.loadUi("ui\\exchange_ratesw.ui")
		self.window.show()
		self.window.le_from.textEdited.connect(self.le_from_edited)
		self.window.le_to.textEdited.connect(self.le_to_edited)
		self.window.btn_graph.clicked.connect(self.btn_graph_push)

	list_of_currency = ['USD','IDR','BGN','ILS','GBP',
						'DKK','CAD','JPY','HUF','RON',
						'MYR','SEK','SGD','HKD','AUD',
						'CHF','KRW','CNY','TRY','HRK',
						'NZD','THB','EUR','NOK','RUB',
						'INR','MXN','CZK','BRL','PLN',
						'PHP','ZAR']

	def init_values(self):
		self.window.cmbbox_to.setCurrentText(self.user_data["currency"])
		req = "https://api.exchangeratesapi.io/latest?base=USD"
		self.rates = (requests.get(req)).json()
		self.rates = self.rates["rates"]
		self.rates["USD"] = 1
		self.window.le_from.setText("1")
		self.window.le_to.setText(str(self.rates[self.user_data["currency"]]))
		self.window.cmbbox_from.currentTextChanged.connect(self.cmbbox_from_changed)
		self.window.cmbbox_to.currentTextChanged.connect(self.cmbbox_to_changed)

		time_to	   = datetime.now()
		time_from  = time_to.timestamp() - (183*24*60*60)
		time_from  = datetime.fromtimestamp(time_from)

		self.window.cmbbox_year_from.setCurrentText(time_from.strftime("%Y"))
		self.window.cmbbox_month_from.setCurrentText(time_from.strftime("%m"))
		self.window.cmbbox_day_from.setCurrentText(time_from.strftime("%d"))

		self.window.cmbbox_year_to.setCurrentText(time_to.strftime("%Y"))
		self.window.cmbbox_month_to.setCurrentText(time_to.strftime("%m"))
		self.window.cmbbox_day_to.setCurrentText(time_to.strftime("%d"))

	def le_input_filter(self, text):
		last_char = text[-1:]
		if last_char == "":
			return True
		if last_char == '.':
			if '.' in text[:-1]:
				self.window.le_from.setText(text[:len(text) - 1])
			return True
		if last_char.isdigit() == False:
			self.window.le_from.setText(text[:len(text) - 1])
			return True
		return False

	def le_from_change(self, text):
		to_currency = self.window.cmbbox_to.currentText()
		val_to = self.rates[to_currency] * float(text)
		self.window.le_to.setText(str(val_to))

	def le_to_change(self, text):
		from_currency = self.window.cmbbox_from.currentText()
		val_to = self.rates[from_currency] * float(text)
		self.window.le_from.setText(str(val_to))

	def le_from_edited(self):
		text = self.window.le_from.text()
		if self.le_input_filter(text):
			return
		self.le_from_change(text)

	def cmbbox_from_changed(self):
		from_currency = self.window.cmbbox_from.currentText()
		req = f"https://api.exchangeratesapi.io/latest?base={from_currency}"
		self.rates = (requests.get(req)).json()
		self.rates = self.rates["rates"]
		self.rates[from_currency] = 1
		text = self.window.le_from.text()
		self.le_from_change(text)

	def le_to_edited(self):
		text = self.window.le_to.text()
		if self.le_input_filter(text):
			return
		self.le_to_change(text)

	def cmbbox_to_changed(self):
		from_currency = self.window.cmbbox_from.currentText()
		to_currency = self.window.cmbbox_to.currentText()
		req = f"https://api.exchangeratesapi.io/latest?base={from_currency}"
		self.rates = (requests.get(req)).json()
		self.rates = self.rates["rates"]
		self.rates[from_currency] = 1
		text = self.window.le_to.text()
		self.le_from_change(text)

	def btn_graph_push(self):
		from_currency = self.window.cmbbox_from.currentText()
		to_currency	  = self.window.cmbbox_to.currentText()

		year_from	  = self.window.cmbbox_year_from.currentText()
		month_from	  = self.window.cmbbox_month_from.currentText()
		day_from	  = self.window.cmbbox_day_from.currentText()

		year_to		  = self.window.cmbbox_year_to.currentText()
		month_to	  = self.window.cmbbox_month_to.currentText()
		day_to	 	  = self.window.cmbbox_day_to.currentText()

		req = f"https://api.exchangeratesapi.io/history?"\
			  f"start_at={year_from}-{month_from}-{day_from}"\
			  f"&end_at={year_to}-{month_to}-{day_to}"\
			  f"&symbols={from_currency},{to_currency}"
		print(req)
		rates = (requests.get(req)).json()
		rates = rates["rates"]

		date_to = datetime.strptime(f"{year_to}{month_to}{day_to}", "%Y%m%d")
		date_from = datetime.strptime(f"{year_from}{month_from}{day_from}", "%Y%m%d")
		rate_list = []
		date_list = []
		while (date_from.timestamp()) < (date_to.timestamp()):
			try:
				date = date_from.strftime("%Y-%m-%d")
				rate_list.append((rates[date])[to_currency])
				date_list.append(date)
			except:
				pass
			date_from  = date_from.timestamp() + (3600 * 24)
			date_from  = datetime.fromtimestamp(date_from)

		x = date_list
		y = rate_list

		plt.xticks(rotation=90)
		plt.xlabel('Даты', fontsize=12)
		plt.ylabel('Курс', fontsize=12)

		plt.plot(x,y)
		plt.show()