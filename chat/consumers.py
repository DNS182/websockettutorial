from channels.consumer import SyncConsumer , AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import json
from asgiref.sync import async_to_sync


#event vaneko k vairaxa tyo ho hai
#print hamro ide ma matrai print gareko to know k vairaxaa

class MySyncConsumer(SyncConsumer):

    def websocket_connect(self,event):
        print("Websocket Connected .....")
        print("Channel Layer : " , self.channel_layer) #layer vaneko db ko host jastai
        print("Channel name : " , self.channel_name) #channel name sabko farak hunxa 
        #so to interact every channel we create group or simply adding channel to group
        #self.channel_layer.group_add is async function so to apply on sync we use asynctosync
        async_to_sync(self.channel_layer.group_add)(
            'pro' , #group ko name
            self.channel_name
            )
        self.send({
            'type': 'websocket.accept'
        }) 
        


    def websocket_receive(self,event):
        async_to_sync(self.channel_layer.group_send)(
            'pro' , 
            {
                'type' : 'chat.message' ,
                'text' : event['text']
            })

    def chat_message(self, event):
        print("Event ..." , event)
        self.send({
            'type' : 'websocket.send' ,
            'text' : event['text']
        })
        
    
    # def websocket_receive(self,event):
    #     self.send({
    #         'type': 'websocket.send',
    #         'text' : 'Client lay yo message Dekhxa'  #yoo text backend bata frontend pass vako we can render this as it is passed as data on event on frontend
    #     }) 
    #     print("Message Received." , event['text'])  #yo eventtext vaneko front end bata user lay pass garekoo





    def websocket_disconnect(self,event):
        print("Websocket DisConnected .....", event)
        async_to_sync(self.channel_layer.group_discard)(   #ko ko vagyo group bata vanera
            'pro' , 
            self.channel_name
            )

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