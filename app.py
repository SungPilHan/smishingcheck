#-*-coding:utf-8-*-
import web
from cheroot import wsgi
from flask import Flask, request, render_template_string
import simplejson as json
import requests

makejson = json.dumps
app = Flask(__name__)
makejson = json.dumps

DEFAULT_PORT_NO = 8888
apivoid_key = "Your apivoid key"

@app.errorhandler(500)
def internal_servererror(error):
	print(" [!]", error)
	return "Internal Server Error", 500

'''
The function handles the authentication mechanism
'''

@app.route('/url', methods=['GET'])
def url():
	url = request.args.get("url")
	long_url = requests.get(url).url
	long_url = long_url.split('/')[2]
	print(long_url)
	print("------------------------")
	data = apivoid_domainrep(apivoid_key, long_url)
	print(data)
	if(data):
		if(data.get('error')):
			return render_template_string(data['error'])
		else:
			if(data['data']['report']['blacklists']['detections'] == 0):
				msg = {"result" : "safe"}
				return makejson(msg)
			else:
				msg = {"result" : "danger"}
				return makejson(msg)
	else:
		return render_template_string("No result")

def apivoid_domainrep(key, host):
	try:
		r = requests.get(url='https://endpoint.apivoid.com/domainbl/v1/pay-as-you-go/?key='+key+'&host='+host)
		return json.loads(r.content.decode())
	except:
		return ""

if __name__ == '__main__':
	port = DEFAULT_PORT_NO
	urls = ("/.*", "app")
	apps = web.application(urls, globals())
	server = wsgi.Server(("0.0.0.0", port),app,server_name='localhost')
	print("The server is hosted on port:",(port))
	
	try:
		server.start()
	except KeyboardInterrupt:
		server.stop()
