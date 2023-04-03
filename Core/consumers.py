import json
import threading
import time

from channels.generic.websocket import WebsocketConsumer
from Core import views

class Console(WebsocketConsumer):
    message = {'status': 0, 'message': None}

    def connect(self):
        self.accept()
        self.client = views.client
        self.console = views.console()
        self.console.read()

    def disconnect(self, code):
        del self.console
        pass

    def receive(self, text_data=None, bytes_data=None):
        print(text_data, bytes_data)
        self.console.write(text_data)
        time.sleep(1)
        self.send(json.dumps(self.console.read()))

class Session(WebsocketConsumer):
    message = {'status': 0, 'message': None}

    def connect(self):
        self.accept()
        self.id = self.scope['url_route']['kwargs']['id']
        self.client = views.client
        self.session, data, self.cid =views.run_session(self.id)
        if  self.session is None:
            self.send(json.dumps({'data':data, 'status': 0}))
        else:
            self.send(json.dumps({'data':data, 'status': 1}))


    def disconnect(self, code):
        self.session.write("background")
        del self.session
        pass
    def receive(self, text_data=None, bytes_data=None):

        if self.session is not None:
            print(text_data)
            self.session.write(text_data)
            timeout= time.time() + 10
            while True:

                if time.time() > timeout:
                    self.send(json.dumps({"data":"Time out","status":0}))
                    break
                data = self.session.read()
                print(data)
                time.sleep(0.2)
                if data['data'] != "":
                    self.send(json.dumps({"data":data['data'],"status":1}))
                    break
        else:
            self.send(json.dumps({"data": self.session.read()['data'], "status": 0}))