from flask import Flask, render_template, request
from subprocess import check_output
from urllib.parse import urlsplit


import re, os, json
import urllib.request
import mimetypes

clients = check_output("arp -a", shell=True).decode()
client_ips = re.findall( r'[0-9]+(?:\.[0-9]+){3}', clients)
clients = client_ips.copy()
actualclients = {}
for client in clients:
	try:
		print(client)
		val = urlopen(client+"/info")
		print(val)
		val = json.loads(val)
		actualclients.setdefault(client, val)
	except:
		pass

print(clients)
def open_uri(url):
	data = None
	print('visiting \'{}\''.format(url))
	try:
		data =  urllib.request.urlopen(url)

	except:
		pass

	return data

def getDomain(url):
	base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
	return base_url

def prepareUrl(url):
	if url.startswith("http://") or url.startswith("https://"):
		return url
	
	else:
		return "http://"+url

def cleanUrl(url):
	url = url.replace("https://", "", 1).replace("http://", "", 1).replace("/", "", 1)
	url = url.split(":")[0]
	return url

def saveFile(filename, data):
	file = open(filename, 'wb')
	file.write(data)
	file.close()

app = Flask(__name__, static_url_path="", static_folder="static/")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/info')
def getInfo():
	myinfo = {'name':'christian'}
	myinfo = json.dumps(myinfo)
	return myinfo

@app.route('/clients')
def getClients():
	clients_info = json.dumps(actualclients)
	return clients_info

@app.route('/goto', methods=['GET'])
def reroute():
	data = "Nothing was recieved!"
	basepath = ""
	content = None

	goto_url = prepareUrl(request.args["url"])
	basename = os.path.basename(goto_url)
	goto_baseurl = getDomain(goto_url)
	clean_baseurl = cleanUrl(goto_baseurl)
	print("url = {}, goto_baseurl = {}, clean_baseurl = {}, basename = {}".format(goto_url, goto_baseurl, clean_baseurl, basename))
	if clean_baseurl in clients:
		content = open_uri(goto_url)
		print(content.headers)
		content_type = content.headers['content-type']
		extension = mimetypes.guess_extension(content_type)

		# mime_type = mime.guess_type(goto_url)
		print(extension)

	else:
		for client in clients:
			content =  open_uri(client+"/goto?url="+goto_url)
			if content != None:
				break

	if content != None:
		data = content
		if basename.strip() == "":
			basename = 'tempfile'+extension
		basepath = "/temp/"+basename
		print("basepath = {}".format(basepath))
		saveFile("static"+basepath, data.read())
	print("basepath = {}".format(basepath))
	return basepath
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
