from pprint import pprint
from twisted.application.internet import TCPServer
from twisted.application.service import Application
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.enterprise import adbapi
import json

class PutPage(Resource):

    def __init__(self):
        self.db = adbapi.ConnectionPool('MySQLdb', user='iot', db='iot', passwd='SmBYWmfaeVyspqfa')

    def render_POST(self, request):
        # pprint(request.__dict__)
        new_data = json.loads(request.content.getvalue())
        for row in new_data:
            pprint(row)
            self.db.runQuery("INSERT INTO data (timestamp, payload) VALUES (%s, %s)", (row['timestamp'], row['payload']))
        return ''

class GetPage(Resource):

    def __init__(self):
        self.db = adbapi.ConnectionPool('MySQLdb', user='iot', db='iot', passwd='SmBYWmfaeVyspqfa')

    def render_GET(self, request):
        #self.db.runQuery("INSERT INTO data (timestamp, payload) VALUES (%s, %s)", (row['timestamp'], row['payload']))
        return 'hello'

root = Resource()
root.putChild("put", PutPage())
root.putChild("api", GetPage())
application = Application("IoT Backend")
TCPServer(8888, Site(root)).setServiceParent(application)
