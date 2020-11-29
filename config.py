import json
import os

CONFIG_FNAME = "config.json"
CONFIG_DEFAULT = {"current_user": None}

def init():
	"""create config file if not exist"""
	if os.path.exists(CONFIG_FNAME):
		return
	save_config(CONFIG_DEFAULT)

def save_config(dict_val):
	"""save config file"""
	with open(CONFIG_FNAME, "w") as fp:
		json.dump(dict_val, fp)

def get_config():
	"""return json config file"""
	with open(CONFIG_FNAME, "r") as fp:
		return json.load(fp)

def get_field(field_name):
	"""return field of json config file"""
	return get_config()[field_name]

def set_field(field_name, field_value):
	"""set field of json config file"""
	data = get_config()
	data[field_name] = field_value
	save_config(data)