from django.db import models
from django.contrib.auth.models import User

class chatRoom(models.Model):
    Room_name=models.CharField(max_length=120,blank=False,default='null')
    
    
    def __str__(self) -> str:
        return self.Room_name

class Messages(models.Model):
    Room=models.ForeignKey(chatRoom,related_name='chat_messages',on_delete=models.CASCADE,default=0)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.CharField(max_length=500)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.author.username}:{self.body}'
   
    
    class Meta:
        ordering=['-created']


class FriendsList(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    Friends_List=models.TextField(null=True)


    

   
