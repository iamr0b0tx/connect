from flask import Flask, render_template, request, abort
from subprocess import check_output
from functions import *

import re, os, json
import mimetypes

myinfo = {'name':'cipherx'}

clients = check_output("arp -a", shell=True).decode()
client_ips = re.findall( r'[0-9]+(?:\.[0-9]+){3}', clients)
host_ips = re.findall( r'Interface: [0-9]+(?:\.[0-9]+){3}', clients)

clients = client_ips.copy()
actualclients = getActualClients(clients)
host_ips = [host_ip.replace("Interface: ", "", 1) for host_ip in host_ips]

print(clients)
print(actualclients)
print(host_ips)

#app instance and config
app = Flask(__name__, static_url_path="", static_folder="static/")

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/info')
def getInfo():
	return json.dumps(myinfo)

@app.route('/clients')
def getClients():
	clients_info = json.dumps(actualclients)
	return clients_info

@app.route('/goto', methods=['GET'])
def reroute():
	data = "Nothing was recieved!"
	basepath = ""
	content = None

	extended = request.args["extended"]
	print("ex", extended)

	goto_url = prepareUrl(request.args["url"])
	basename = os.path.basename(goto_url)
	goto_baseurl = getDomain(goto_url)
	clean_baseurl = cleanUrl(goto_baseurl)
	url_root = cleanUrl(getDomain(request.base_url))
	print("\nurl_root = {}\nurl = {}\ngoto_baseurl = {}\nclean_baseurl = {}\nbasename = {}".format(url_root, goto_url, goto_baseurl, clean_baseurl, basename))

	if clean_baseurl in clients:
		content = open_uri(goto_url)
		if content != None:
			print("url request resolved by imediate client = {}".format(clean_baseurl))
		# print(content.headers)
		# content_type = content.headers['content-type']
		# extension = mimetypes.guess_extension(content_type)

		# mime_type = mime.guess_type(goto_url)

	else:
		if url_root in host_ips:
			print("looped!")
			return "[looping]"

		else:
			print("checking if clients can route url resolve")
			for client in clients:
				content =  open_uri("{}/goto?url={}&extended=[{}]".format(bindUrl(client), goto_url, myinfo["name"]))
				if content != None:
					print("url request resolved by client = {}".format(client))
					break

	if content != None:
		data = content
		if extended != myinfo["name"] or extended == "[0]":
			if basename.strip() == "":
				basename = 'tempfile'+extension
			basepath = "/temp/"+basename
			print("basepath = {}".format(basepath))
			saveFile("static"+basepath, data)
			print("basepath = {}".format(basepath))
			return basepath

		else:
			return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
