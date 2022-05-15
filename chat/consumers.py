from channels.consumer import SyncConsumer , AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import json


#event vaneko k vairaxa tyo ho hai
#print hamro ide ma matrai print gareko to know k vairaxaa

class MySyncConsumer(SyncConsumer):

    def websocket_connect(self,event):
        self.send({
            'type': 'websocket.accept'
        }) 
        print("Websocket Connected .....")


    def websocket_receive(self,event):
        for i in range(50):
            self.send({
                'type': 'websocket.send',
                'text' : json.dumps({'count' : i})   
            }) 
            sleep(1)
    
    # def websocket_receive(self,event):
    #     self.send({
    #         'type': 'websocket.send',
    #         'text' : 'Client lay yo message Dekhxa'  #yoo text backend bata frontend pass vako we can render this as it is passed as data on event on frontend
    #     }) 
    #     print("Message Received." , event['text'])  #yo eventtext vaneko front end bata user lay pass garekoo





    def websocket_disconnect(self,event):
        print("Websocket DisConnected .....", event)
        raise StopConsumer()


# AsyncConsumer use grad async ra await use garna paryoo

class MyAsyncConsumer(AsyncConsumer):
    
    async def websocket_connect(self,event):
        await self.send({
            'type': 'websocket.accept'
            }) 
        print("Websocket Connected .....")


    async def websocket_receive(self,event):
        await self.send({
            'type': 'websocket.send',
            'text' : 'Client lay yo message Dekhxa'  
        })
        print("Message Received." , event['text'])


    async def websocket_disconnect(self,event):
        raise StopConsumer()