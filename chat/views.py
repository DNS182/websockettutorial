from django.shortcuts import get_object_or_404, render
from . models import Group , Chat

# Create your views here.
def index(request , room_name):
    group = Group.objects.filter(name = room_name).first()
    chats =[]
    if group is not None :
        chats = Chat.objects.filter(group = group)

    else:
        group = Group(name = room_name)
        group.save()
    
    return render(request , 'index.html' , {'room' : room_name , 'chats':chats})