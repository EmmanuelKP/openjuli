# !/usr/bin/python
'''Open JULI backend code '''
import os
import re
import hashlib
import random
import requests
import mysql.connector
from cryptography.fernet import Fernet

session = requests.Session()

env = {}
try:
	with open(".env") as f:
		while True:
			x = f.readline()
			if x:
				x = x.strip()
				if not x.startswith("#"):
					key,value = x.split("=")
					env[key] = value
			else:
				break
except:
	print("Failed to read env file")
	os._exit(0)

#Global variables and configuation(from env file)
DB_FILE = env["DB_FILE"]
SECRET_KEY = (env["SECRET_KEY"] + "=").encode()
OPENAI_KEY = env["OPENAI_KEY"]

def DB_init():
	'''Create db if it doesn't exist'''
	#Redacted
	pass



#<Main code starts here>
#Initialize encryption
fernet = Fernet(SECRET_KEY)

def gen_salt(length):
	'''Generate salt for hashing password'''
	charSet = "abcdefghijklmnopqrstuvwxyz1234567890"
	salt = ""
	for i in range(length):
		r1 = random.randint(0,len(charSet)-1)
		c = charSet[r1]
		if c.isalpha():
			r2 = random.randint(0,1)
			if r2 == 0:
				salt += c
			else:
				salt += c.upper()
		else:
			salt += c
	return salt


DB_init()


#Creating users table
#The table user has these fields by default
#	Name of user - 256 characters
#	Email - 320 characters
#	Password - stored as hash(sha-256)
#	Salt - 32 char
#	Prompt - 3000 char limit(to store prompts from user)

def db():
	#Redacted
	return []

def create_account(name,email,password):
	'''Create user account'''
	accountExists = False
	for i in db():
		e = i[1]
		if e == email:
			accountExists = True
			break
	if not accountExists:
		salt = gen_salt(32)
		p = hashlib.sha256(str(password + salt).encode("UTF-8")).hexdigest()
		data = db()
		data.append([name,email,p,salt,[]])
		#Redacted
		pass
		return True
	else:
		return False

def signin_account(data):
	'''Check whether the provided credentials are correct and authenticate'''
	email = data["email"].lower()
	password = data["password"]
	matches = False
	sessionID = ""
	for i in db():
		e,p,s = i[1],i[2],i[3]
		pHash = hashlib.sha256(str(password + s).encode("UTF-8")).hexdigest()
		if e == email and p == pHash:
			matches = True
			sessionID = fernet.encrypt("{}<>{}".format(email,pHash).encode()).decode()
			break
	return (matches,sessionID)

def validate_token(token):
	'''Validate token in the client side'''
	validated = False
	try:
		email,password = fernet.decrypt(token.encode()).decode().split("<>")
		for i in db():
			u,e,p = i[0],i[1],i[2]
			if e == email and p == password:
				validated = True
				break
		return (validated,u,e)
	except:
		return (False,"","")


#Functions that handle requests
def validate_signup(data):
	'''Check and report errors in user supplied information'''
	'''Validates signup information provided by the user'''
	errors = ""
	#Name
	if not str(data["name"]).replace(" ","SEP").isalpha():
		errors += "Name should only contain alphabets!. "
	#Email
	emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
	if not re.fullmatch(emailRegex,data["email"]):
		errors += "Invalid email!. "

	#Checking length of data
	if len(data["name"]) > 256:
		errors += "Name should only have 256 characters!. "
	if len(data["email"]) > 320:
		errors += "Email should only have 320 characters!. "

	if errors == "":
		acCreated = create_account(data["name"],data["email"],data["password"])
		if not acCreated:
			errors += "Account already exists with the email!. "
			return (False,errors)
		return (True,errors)
	else:
		return (False,errors)

def chat(data,cookie):
	input = data.get("user_input")
	email = validate_token(cookie)[2]
	data = db()
	#Redacted
	pass

def allowedIP(IP):
	#Redacted
	pass