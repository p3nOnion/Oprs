import json
import threading
import time

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from Core import views

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "message"#self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
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
        self.session = self.client.sessions.session(str(self.id))
        data = self.session.read()
        print(data)
        if  self.session is None:
            self.send(json.dumps({'data':data, 'status': 0}))
        else:
            self.send(json.dumps({'data':data, 'status': 1}))


    def disconnect(self, code):
        # self.session.write("background")
        del self.session
        pass
    def receive(self, text_data=None, bytes_data=None):

        if self.session is not None:
            self.session.write(text_data)
            data = self.session.read()
            print(data)
            if data!="":
                self.send(json.dumps({"data": data, "status": 1}))
            else:
                self.send(json.dumps({"data": "", "status": 0}))
            # print(text_data)
            # self.session.write(text_data)
            # timeout = time.time() + 10
            # while True:
            #
            #     if time.time() > timeout:
            #         self.send(json.dumps({"data":"Time out","status":0}))
            #         break
            #     data = self.session.read()
            #     print(data)
            #     time.sleep(0.2)
            #     if data['data'] != "":
            #         self.send(json.dumps({"data":data['data'],"status":1}))
            #         break
        else:
            self.send(json.dumps({"data": "End!", "status": 0}))