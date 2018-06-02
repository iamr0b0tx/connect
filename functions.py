from constants import *
from urllib.parse import urlsplit

import urllib.request
import json

def getActualClients(clients):
	actualclients = {}
	for client in clients:
		try:
			url = bindUrl(client)+"/info"
			val = urllib.request.urlopen(url)
			val = val.read().decode()
			val = json.loads(val)
			actualclients.setdefault(client, val)
		except Exception as e:
			#print(e)
			pass

	return actualclients

def bindUrl(url):
	return "{}:{}".format(prepareUrl(url), str(PORT))

def open_uri(url):
	data = None
	print('visiting \'{}\''.format(url))
	try:
		data =  urllib.request.urlopen(url)
		data = data.read()
		if data.decode() == "[looping]":
			data = None

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
