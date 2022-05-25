from unicodedata import name
from channels.consumer import SyncConsumer , AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import json
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from chat.models import Group , Chat


#event vaneko k vairaxa tyo ho hai
#print hamro ide ma matrai print gareko to know k vairaxaa

#async_to_sync used on sync cause its already on async function

class MySyncConsumer(SyncConsumer):

    def websocket_connect(self,event):
        print("Websocket Connected .....")
        print("Channel Layer : " , self.channel_layer) #layer vaneko db ko host jastai
        print("Channel name : " , self.channel_name) #channel name sabko farak hunxa 
        #so to interact every channel we create group or simply adding channel to group
        #self.channel_layer.group_add is async function so to apply on sync we use asynctosync
        group_name = self.scope['url_route']['kwargs']['groupname']
        async_to_sync(self.channel_layer.group_add)(
            group_name , #group ko name
            self.channel_name
        )
        self.send({
            'type': 'websocket.accept'
        }) 
        
    

    def websocket_receive(self,event):
        # print("User ko naam : " , self.scope['user'])
        data = json.loads(event['text'])
        group_name = self.scope['url_route']['kwargs']['groupname']
        group = Group.objects.get(name = group_name)
        chat = Chat(
                chatmsg = data['msg'] ,
                group = group
                )
        
        data['user'] = self.scope['user'].username
        print(data)
        if self.scope['user'].is_authenticated:
            async_to_sync(self.channel_layer.group_send)(
                group_name , 
                {
                    'type' : 'chat.message' ,
                    'text' : json.dumps(data)
                })
            print(event['text'])
            chat.save()
        else:
            self.send({
            'type' : 'websocket.send' ,
            'text' : json.dumps({'msg': 'User Not Logged' , 'user' : 'guest'})
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
        group_name = self.scope['url_route']['kwargs']['groupname']
        print("Websocket DisConnected .....", event)
        async_to_sync(self.channel_layer.group_discard)(   #ko ko vagyo group bata vanera
            group_name , 
            self.channel_name
            )

        raise StopConsumer()


# AsyncConsumer use grad async ra await use garna paryoo

class MyAsyncConsumer(AsyncConsumer):
    
    async def websocket_connect(self,event):
        await self.channel_layer.group_add(
            'pro' , #group ko name
            self.channel_name
            )
        await self.send({
            'type': 'websocket.accept'
        }) 
        
#asynchronous ma garda models vako thau ma database_sync_to_async garnu parxa to do "from channels.db import database_sync_to_async"

    async def websocket_receive(self,event):
        data = json.loads(event['text'])
        group_name = self.scope['url_route']['kwargs']['groupname']
        group = await database_sync_to_async(Group.objects.get)(name = group_name)
        chat = Chat(
                chatmsg = data['msg'] ,
                group = group
                )
        await database_sync_to_async(chat.save)()
        await self.channel_layer.group_send(
            'pro' , 
            {
                'type' : 'chat.message' ,
                'text' : event['text']
            })

    async def chat_message(self, event):
        print("Event ..." , event)
        await self.send({
            'type' : 'websocket.send' ,
            'text' : event['text']
        })
        

    async def websocket_disconnect(self,event):
        print("Websocket DisConnected .....", event)
        await self.channel_layer.group_discard(   #ko ko vagyo group bata vanera
            'pro' , 
            self.channel_name
            )

        raise StopConsumer()