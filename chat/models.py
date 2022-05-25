from django.db import models

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=25)
     
    def __str__(self):
        return self.name


class Chat(models.Model):
    chatmsg = models.CharField(max_length=1500)
    timedate = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group , on_delete=models.CASCADE)

    def __str__(self):
        return self.chatmsg[0:150]
