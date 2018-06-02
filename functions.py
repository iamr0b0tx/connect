from constants import *
from urllib.parse import urlsplit
from urllib.request import urlretrieve

import urllib.request
import json, requests, os

#constants
FILE_TRACKER_INIT = "{'part_length':'', 'path':''}"

def getFileContents(filepath):
	file = open(filepath, 'rb')
	r = file.read()
	file.close()
	return r


def setFileContents(filepath, data):
	file = open(filepath, 'wb')
	file.write(data)
	file.close()
	return True

def readFile(filepath):
	file = open(filepath, 'r')
	r = file.read()
	file.close()
	return r

def writeFile(filepath, data):
	file = open(filepath, 'w')
	file.write(data)
	file.close()
	return True

def getFileName(filepath):
	return os.path.splitext(os.path.basename(filepath))[0]

def saveChunk(file, chunk):
	filename = getFileName(file)
	if os.path.exists(filename):
		pass

	else:
		os.mkdir(filename)

	file_tracker_path = "{}/{}".format(filname, filename+"_tracker.json")

	try:
		file_tracker_data = readFile(file_tracker_path)

	except Exception as e:
		print(e)
		file_tracker_data = FILE_TRACKER_INIT
		writeFile(file_tracker_path, file_tracker_data)

	file_tracker = json.loads(file_tracker_data)
	setFileContents(file_tracker["path"]+str(file_tracker["part_length"]+1), chunk)
	file_tracker["part_length"] += 1
	writeFile()

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
		print(data[:10])
		if data.decode() == "[looping]":
			data = None

	except:
		pass

	return data

def open_uri2(url):
	data = None
	print('visiting \'{}\''.format(url))
	try:
		data =  requests.get(url, stream=True)
		chunks = data.iter_content(chunk_size=1024)
		first_line = next(chunks)
		for chunk in chunks:
			saveChunk(file, chunk)

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
