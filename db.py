import sqlite3

DB_NAME = "nameless_bank.db"

class TABLE_DATA:
	def __init__(self, name):
		self.DATA = {"name": name}

	def __getitem__(self, key):
		return self.DATA[key]

class __TB_USERDATA(TABLE_DATA):
	def __init__(self, name):
		super().__init__(name)

		self.DATA["username_max_lenght"]		 = 128
		self.DATA["password_max_lenght"]		 = 512 #hash md5
		self.DATA["currency_max_lenght"]		 = 64
		self.DATA["control_question_max_lenght"] = 128
		self.DATA["avatar_path_max_lenght"]		 = 247
		self.DATA["email_address_max_lenght"]	 = 128
		self.DATA["phone_number_max_lenght"]	 = 32
		self.DATA["sex_max_lenght"]				 = 16

		self.FIELDS_LIST = ["id", "username", "password", "currency",
					   		"control_question", "control_question_answer",
					   		"avatar_path", "phone_number", "sex", "email_address",
					   		"email_valid", "reg_date", "balance"]
		self.FIELDS_TYPES = [
			f"INTEGER PRIMARY KEY",	#id
			f"CHAR({self.DATA['username_max_lenght']})",		 #username
			f"CHAR({self.DATA['password_max_lenght']})",		 #password
			f"CHAR({self.DATA['currency_max_lenght']})",		 #currency
			f"CHAR({self.DATA['control_question_max_lenght']})", #control_question
			f"CHAR({self.DATA['control_question_max_lenght']})", #control_question_answer
			f"CHAR({self.DATA['avatar_path_max_lenght']})",		 #avatar_path
			f"CHAR({self.DATA['phone_number_max_lenght']})",	 #phone_number
			f"CHAR({self.DATA['sex_max_lenght']})", 			 #sex
			f"CHAR({self.DATA['email_address_max_lenght']})",	 #email_address
			f"INTEGER",		#email_valid, bool
			f"TIMESTAMP",	#reg_date, datetime
			f"REAL"			#balance
		]

		self.FIELDS_TYPES_DICT = {}
		self.FIELDS_SQLITE3 = ""
		for i in range(len(self.FIELDS_LIST)):
			field_name = self.FIELDS_LIST[i]
			field_type = self.FIELDS_TYPES[i]
			self.FIELDS_TYPES_DICT[field_name] = field_type
			self.FIELDS_SQLITE3 += f"{field_name} {field_type},"
		self.FIELDS_SQLITE3 = self.FIELDS_SQLITE3[:-1]

		self.FIELDS_WITHOUT_PRIMARY_KEY_LIST = self.FIELDS_LIST[1:]
		self.FIELDS_SQLITE3_WITHOUT_ID = ""
		for i in self.FIELDS_WITHOUT_PRIMARY_KEY_LIST:
			self.FIELDS_SQLITE3_WITHOUT_ID += i + ", "
		self.FIELDS_SQLITE3_WITHOUT_ID = self.FIELDS_SQLITE3_WITHOUT_ID[:-2]

		self.ARG_SEQUENCE = ""
		for i in range(len(self.FIELDS_LIST)):
			self.ARG_SEQUENCE += "?, "
		self.ARG_SEQUENCE = self.ARG_SEQUENCE[:-2]

		self.ARG_SEQUENCE_WITHOUT_ID = self.ARG_SEQUENCE[3:]

class __TB_TRANSFERDATA(TABLE_DATA):
	def __init__(self, name):
		super().__init__(name)
		self.DATA["currency_max_lenght"] = 64
		self.DATA["message_max_lenght"]  = 256

		self.FIELDS_LIST = ["id", "id_sender", "id_receiver", "currency",
					   		"value", "commission", "date", "msg"]
		self.FIELDS_TYPES = [
			f"INTEGER PRIMARY KEY",	#id
			f"INTEGER", 			#id_sender
			f"INTEGER", 			#id_receiver
			f"CHAR({self.DATA['currency_max_lenght']})", #currency
			f"REAL",	  #value
			f"REAL",	  #commission
			f"TIMESTAMP", #date, datetime
			f"CHAR({self.DATA['message_max_lenght']})", #msg
		]

		self.FIELDS_TYPES_DICT = {}
		self.FIELDS_SQLITE3 = ""
		for i in range(len(self.FIELDS_LIST)):
			field_name = self.FIELDS_LIST[i]
			field_type = self.FIELDS_TYPES[i]
			self.FIELDS_TYPES_DICT[field_name] = field_type
			self.FIELDS_SQLITE3 += f"{field_name} {field_type},"
		self.FIELDS_SQLITE3 = self.FIELDS_SQLITE3[:-1]

		self.FIELDS_WITHOUT_PRIMARY_KEY_LIST = self.FIELDS_LIST[1:]
		self.FIELDS_SQLITE3_WITHOUT_ID = ""
		for i in self.FIELDS_WITHOUT_PRIMARY_KEY_LIST:
			self.FIELDS_SQLITE3_WITHOUT_ID += i + ", "
		self.FIELDS_SQLITE3_WITHOUT_ID = self.FIELDS_SQLITE3_WITHOUT_ID[:-2]

		self.ARG_SEQUENCE = ""
		for i in range(len(self.FIELDS_LIST)):
			self.ARG_SEQUENCE += "?, "
		self.ARG_SEQUENCE = self.ARG_SEQUENCE[:-2]

		self.ARG_SEQUENCE_WITHOUT_ID = self.ARG_SEQUENCE[3:]

TB_USERDATA = __TB_USERDATA("table_user_data")
TB_TRANSFERDATA = __TB_TRANSFERDATA("table_transfer_data")




def create_table(table_data):
	conn = sqlite3.connect(DB_NAME)
	conn.execute(f"""CREATE TABLE IF NOT EXISTS {table_data["name"]}
					({table_data.FIELDS_SQLITE3})""")
	conn.commit()
	conn.close()

def read_table(table_data):
	conn = sqlite3.connect(DB_NAME)
	ret = conn.execute(f"""SELECT * FROM {table_data["name"]}""")
	ret = [i for i in ret]
	conn.close()
	return ret

def read_table_get_dict(table_data):
	tb_data = read_table(table_data)
	result = []
	for i in tb_data:
		_dict = {}
		for j in range(len(i)):
			_dict[table_data.FIELDS_LIST[j]] = i[j]
		result.append(_dict)
	return result

def read_table_get_dict_by_field(table_data, column_name, value):
	for i in read_table_get_dict(table_data):
		if i[column_name] == value:
			return i

def read_table_column(table_data, column_name):
	conn = sqlite3.connect(DB_NAME)
	ret = conn.execute(f"""SELECT {column_name} FROM {table_data["name"]}""")
	ret = [i[0] for i in ret]
	conn.close()
	return ret

def read_table_row_by_field(table_data, field_name, field_value):
	_dict = read_table_get_dict(table_data)
	for i in _dict:
		if field_value == i[field_name]:
			return i
	return None

def replace_table_row_field(table_data, row, value, value_name):
	conn = sqlite3.connect(DB_NAME)
	conn.execute(f"""UPDATE {table_data["name"]}
				     SET {value_name}="{value}" where id={row}""")
	conn.commit()
	conn.close()

def write_table(table_data, *args):
	conn = sqlite3.connect(DB_NAME)
	conn.execute(f"""INSERT INTO {table_data["name"]}
					({table_data.FIELDS_SQLITE3_WITHOUT_ID})
				VALUES ({table_data.ARG_SEQUENCE_WITHOUT_ID})""",
				args)
	conn.commit()
	conn.close()

create_table(TB_USERDATA)
create_table(TB_TRANSFERDATA)