import hashlib

def make_hash(username, password):
	salt = hashlib.md5(bytes(username, "utf-8"))
	md5  = hashlib.sha512(bytes(password + salt.hexdigest(), "utf-8"))
	return md5.hexdigest()