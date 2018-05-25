import urllib.request
import mimetypes

url = 'http://192.168.137.132:33455/web/srcimg/img_home_phone.png'

response = urllib.request.urlopen(url)
content_type = response.headers['content-type']
extension = mimetypes.guess_extension(content_type)
