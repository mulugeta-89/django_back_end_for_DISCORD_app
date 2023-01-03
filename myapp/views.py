from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.
# from django.http import HttpResponse
# rooms = [
#     {"id": 1, "desc": "Let's learn python"},
#     {"id": 2, "desc": "Design with us"},
#     {"id": 3, "desc": "With much less cose"}
# ]
def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "The user does not exist")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "The username or password is not correct")
            
    page = 'login'
    context={'page': page}
    return render(request, "login-page.html", context)

def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration!")
    context = {"page":page, "form":form}
    return render(request, 'login-page.html', context)

def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    rooms = Room.objects.filter(Q(topic__name__icontains=q)  | Q(name__icontains=q) | Q(description__icontains = q)) # you could use iexact to filter for the exact world
    topics = Topic.objects.all()
    room_count = rooms.count
    roomMessages = Message.objects.filter(room__topic__name__icontains=q)
    print(request.GET)
    return render(request, "home.html", {"rooms": rooms, "topics": topics, "room_count":room_count,"roomMessages": roomMessages})

def userPage(request, userId):
    user = User.objects.get(id=userId)
    rooms = user.room_set.all()
    roomMessages = user.message_set.all()
    topics = Topic.objects.all()
    context = {"user": user,"rooms":rooms, "roomMessages":roomMessages, "topics":topics}
    return render(request, "user_page.html", context)


def room(request, roomId):
    room = Room.objects.get(id=roomId)
    if request.method == 'POST':
        Message.objects.create (
            User = request.user,
            room = room,
            body = request.POST.get('body')
            )
        room.partcipants.add(request.user)
        return redirect("room",roomId=room.id)
    participants = room.partcipants.all()
    
    
    room_messages = room.message_set.all()
    return render(request, "room.html", {"room": room, "room_messages":room_messages, 'participants':participants})

@login_required(login_url="login")
def createRoom(request):
    form= RoomForm()
    context = {"form": form}
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.host = request.user
            form.save()
        return redirect("home")
    return render(request, "form-room.html", context)

@login_required(login_url='login')
def updateRoom(request, roomId):
    room = Room.objects.get(id = roomId)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("You are not allowed to do this!")
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid:
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "form-room.html", context)

@login_required(login_url='login')
def deleteRoom(request, roomId):
    room = Room.objects.get(id=roomId)
    if request.user != room.host:
        return HttpResponse("You are not allowed to do this!")
    if request.method == 'POST':
        room.delete()
        print(request.user)
        return redirect("home")
    return render(request, "delete-room.html", {"obj":room})
def logoutUser(request):
    logout(request )
    return redirect("home")

@login_required(login_url='login')
def deleteMessage(request, mesgId):
    message = Message.objects.get(id=mesgId)
    if request.user != message.User:
        return HttpResponse("You are not allowed to do this operation!")
    if request.method == 'POST':
        message.delete()
        return redirect("home")
    
    return render(request, 'delete-room.html', {"obj":message})