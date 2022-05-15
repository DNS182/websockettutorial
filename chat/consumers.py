from channels.consumer import SyncConsumer , AsyncConsumer
from channels.exceptions import StopConsumer


class MySyncConsumer(SyncConsumer):

    def websocket_connect(self,event):
        self.send({
            'type': 'websocket.accept'
        }) 
        print("Websocket Connected .....")


    def websocket_receive(self,event):
        self.send({
            'type': 'websocket.send',
            'text' : 'Client lay yo message Dekhxa'
        }) 
        print("Message Received." , event['text'])


    def websocket_disconnect(self,event):
        raise StopConsumer()