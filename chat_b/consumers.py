from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from main.models import Messages,chatRoom,FriendsList
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
import json
from django.contrib.auth.models import User

class chat_consumer(WebsocketConsumer):
    def connect(self):
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_group=f"chat_{self.room_name}"
       
        async_to_sync(self.channel_layer.group_add)(
            self.room_group,self.channel_name
        )
        

        self.accept()

        self.send(text_data=json.dumps({'status':'Conection is established'}))
    
    def disconnect(self, code):
        print({'status':'Disconnected succesfully'})
        pass
    
    def receive(self, text_data):
       messages=json.loads(text_data)
       chat_messages=messages['message']
       author=messages['author']
       room_id=messages['room_id']
       room=get_object_or_404(chatRoom,Room_name=room_id)
       author=get_object_or_404(User,username=author)
       new=Messages.objects.create(body=chat_messages,author=author,Room=room)
       new.save()
       async_to_sync(self.channel_layer.group_send)(
           self.room_group, {"type": "chat.message", "message": messages}
           )
       

    def chat_message(self, event):
        messages = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"chat_messages": messages}))
        