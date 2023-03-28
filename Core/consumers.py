import json
import time

from channels.generic.websocket import WebsocketConsumer
from Core import views

class Console(WebsocketConsumer):
    message = {'status': 0, 'message': None}

    def connect(self):
        self.accept()
        query_string = self.scope.get('query_string')
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
        query_string = self.scope.get('query_string')
        self.client = views.client
        self.session, data = views.run_session(1)
        if  self.session is None:
            self.send(json.dumps({'data':data, 'status': 0}))
            self.close()
        else: self.send(json.dumps({'data':data, 'status': 1}))

    def disconnect(self, code):
        del self.session
        pass
    def receive(self, text_data=None, bytes_data=None):
        if self.session is not None:
            self.session.write(text_data)
            self.send(json.dumps(self.session.read()))
        pass
