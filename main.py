import os
import requests
from flask import Flask, render_template, redirect, jsonify, request, make_response
from gevent.pywsgi import WSGIServer
from replit import db
import json
import uuid
code = False
username = ''
gid = ''
app = Flask(__name__)
class User(object):
	def __init__(self, email, password, name):
		self.email = email
		self.password = password
		self.name = name
		self.randcoins = 0
		self.id = uuid.uuid1()
	def signup(self):
		db[self.name] = {'id':self.id, 'points':self.randcoins, 'email':self.email, 'password':self.password, 'name':self.name}
		db[self.id] = db[self.name]
headers = {
	"Authorization": f"token {os.environ['API']}"
}
@app.route('/')
def main():
	return render_template('main.html')
@app.route("/gist")
def hello_world():
	def getgist():
		gist = requests.get('https://api.github.com/gists/public?per_page=1', headers=headers).json()
		username = gist[0]['owner']['login']
		gid = gist[0]['id']
		print(gist)
		return render_template("index.html", username=username, gid=gid)
	return getgist()
@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
	message = str()
	paid = request.args.get('paid')
	if paid == 'paid':
		message='Press  to  Hide  IP:'
		on = 'document.location="get_my_ip"'
		but = 'H i d e'
		hide = 'visible'
	else:
		message='Press  to  Show  IP:'
		paid = 'ip'
		on = 'document.location="get_my_ip?paid=paid"'
		but = 'S h o w'
		hide = 'visible'
	ip = str(request.access_route[0])
	return render_template('ip.html', data=ip, paid=paid, message=message, onclaclk=on, butmes=but, hide=hide)
@app.route('/signin')
def usersignin():
	if request.cookies.get('userID') != None:
		usid = request.cookies.get('userID')
		usercheck = db[usid]
		email, password, name = usercheck['email'], usercheck['password'], usercheck['name']
		return f'login through cookie ({usid})'
	correctemail = False
	correctpassword = False
	email, password, name = request.args.get('email'), request.args.get('password'), request.args.get('name')
	usercheck = db[name]
	if usercheck['email'] == email:
		correctemail = True
	if usercheck['password'] == password:
		correctpassword = True
	if correctemail == True and correctpassword == True:
		return 'login true'
	else:
		return 'login false'
@app.route('/signup')
def signup():
	email, password, name = request.args.get('email'), request.args.get('password'), request.args.get('name')
	if email == None or password == None or name == None:
		return 'some values are missing'
	user = User(email, password, name)
	user.signup()
	usid = user.id
	resp = make_response(render_template('readcookie.html'))
	resp.set_cookie('userID', usid)

	return resp

@app.route('/delacc')
def delacc():
	name = request.args.get('name')
	try:
		del db[name]

	except:
		return(f"keyerror:  '{name}' doesnt exist")
os.system('pip freeze > requirements.txt')
http_server = WSGIServer(('', 8080), app)
http_server.serve_forever()
