# !/usr/bin/python
import backend
from flask import Flask,send_from_directory,make_response,render_template,request,redirect,render_template_string,jsonify
from os import path

#App configuration
app = Flask(__name__,static_folder="static")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0



#Functions
def display(template,username=""):
	if template == "course.html":
		response = make_response(render_template(template,username=username))
	else:
		response = make_response(render_template(template))
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	response.headers["Pragma"] = "no-cache"
	response.headers["Expires"] = "0"
	if request.cookies.get("SESSIONID") is None:
		response.set_cookie("SESSIONID",value="")
	return response

def set_auth_token(token):
	response = make_response(redirect("/course"))
	response.set_cookie("SESSIONID",value=token)
	return response

def error_msg(msg):
	return render_template_string("<script>alert('Error: {}');window.history.back();</script>".format(msg))



#Static page rendering
@app.route("/favicon.ico")
def favicon():
	return send_from_directory(path.join(app.root_path, "static"),"favicon.ico", mimetype="image/vnd.microsoft.icon")

@app.route("/style.css")
def stylesheet():
	return send_from_directory(path.join(app.root_path, "static"),"style.css", mimetype="text/css")

@app.route("/")
def home():
	return display("index.html")

@app.route("/signin",methods=["GET","POST"])
def signin():
	if request.method == "POST":
		authenticated,token = backend.signin_account(request.form)
		if authenticated:
			return set_auth_token(token)
		else:
			return error_msg("Invalid username or password!")
	else:
		if backend.validate_token(request.cookies.get("SESSIONID"))[0]:
			return redirect("/course")
		else:
			return display("signin.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
	if request.method == "POST":
		validated,message = backend.validate_signup(request.form)
		if validated:
			return render_template_string("<script>alert('Account was successfully created!');window.location.href='/signin';</script>")
		else:
			return error_msg(message)
	else:
		return display("signup.html")

@app.route("/course")
def course():
	validated,username,email = backend.validate_token(request.cookies.get("SESSIONID"))
	if validated:
		return display("course.html",username=username)
	else:
		return redirect("/signin")

@app.route("/chat",methods=["GET","POST"])
def chat():
	if request.method == "POST":
		if backend.validate_token(request.cookies.get("SESSIONID"))[0]:
			return jsonify(backend.chat(request.json,request.cookies.get("SESSIONID")))
		else:
			return redirect("/signin")
	else:
		return redirect("/signin")

@app.route("/signout")
def signout():
	response = make_response(redirect("/signin"))
	response.set_cookie("SESSIONID",value="")
	return response

@app.errorhandler(404)
def not_found(e):
	return render_template("404.html")

#Start server
app.run(host="0.0.0.0", port=5000, debug=False)