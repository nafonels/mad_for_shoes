import sys
import json
import urllib.request

page_name = "shoeswhat"
app_id = "200970590713970"
app_secret = "220f4be97009b81ef75ba8ac2ce1227d"
access_token = app_id + "|" + app_secret

base = "https://graph.facebook.com/v2.8"
node = "/"+page_name
parameters="/?access_token=%s" % access_token
url = base + node + parameters

req = urllib.request.Request(url)

try:
    response = urllib.request.urlopen(req)
    if response.getcode() == 200:
        data = json.loads(response.read().decode('utf-8'))
        page_id=data['id']
        print("%s Facebook Numeric ID : %s" % (page_name, page_id))
except Exception as e:
    print(e)