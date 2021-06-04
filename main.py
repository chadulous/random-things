import requests
from flask import Flask, render_template, redirect, jsonify, request
from gevent.pywsgi import WSGIServer
import json
import os
code = False
username = ''
gid = ''
app = Flask(__name__)
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
	getgist()
	return render_template("index.html", username=username, gid=gid)
@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
	message = str()
	paid = request.args.get('paid')
	if paid == 'paid':
		message='Thanks for "paying"!'
		on = ''
		but = ''
		hide = 'hidden'
	else:
		message= f'Pay 99 million dollars to get your Ip:'
		paid = 'ip'
		on = 'document.location="get_my_ip?paid=paid"'
		but = 'Buy ipget Premium'
		hide = 'visible'
	ip = str(request.access_route[0])
	return render_template('ip.html', data=ip, paid=paid, message=message, onclaclk=on, butmes=but, hide=hide)
http_server = WSGIServer(('', 8080), app)
http_server.serve_forever()
