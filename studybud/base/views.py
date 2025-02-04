from django.shortcuts import render, redirect
from .models import Room, Topic, User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# from .form import RoomForm

# Create your views here.


def index(request):

    topics = Topic.objects.all()
    room_count = Room.objects.count()

    q = request.GET.get('q', '').strip()

    if q:
        # Implement a Q lookup for different fields
        rooms = Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        ).order_by("-created")
        room_count = rooms.count()
    else:
        rooms = Room.objects.all().order_by("-created")

    return render(request, "index.html", {"rooms": rooms, "topics": topics, "room_count": room_count})


def login_page(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Username or password wrong.")

    return render(request, "login_register.html", {"page": page})


def logout_page(request):
    logout(request)
    return redirect('login_page')


def register(request):

    form = UserCreationForm()

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')

    return render(request, 'login_register.html', {"form": form})


def room(request, id):
    context = Room.objects.get(id=int(id))
    return render(request, "room.html", {"room": context})


@login_required(login_url='login_page')
def create(request):

    hosts = User.objects.all()
    topics = Topic.objects.all()

    if request.method == "POST":

        host_id = request.POST.get('host')
        topic_id = request.POST.get('topic')
        name = request.POST.get('name')
        description = request.POST.get('desc')

        host = User.objects.get(id=host_id)
        topic = Topic.objects.get(id=topic_id)

        room = Room(host=host, topic=topic, name=name, description=description)
        room.save()

        return redirect('index')

    return render(request, "create.html", {
        "topics": topics,
        "hosts": hosts
    })


@login_required(login_url='login_page')
def update(request, id):

    room = Room.objects.get(id=int(id))
    topics = Topic.objects.all()

    if request.user != room.host:
        messages.error(request, "You're nor allowed to perform this action.")
        return

    if request.method == "POST":

        topic_id = request.POST.get('topic')
        name = request.POST.get('name')
        description = request.POST.get('desc')

        topic = Topic.objects.get(id=topic_id)

        room.topic = topic
        room.name = name
        room.description = description

        room.save()

        return redirect('room', id=room.id)

    return render(request, "update.html", {"room": room, "topics": topics})


@login_required(login_url='login_page')
def delete(request, id):

    room = Room.objects.get(id=id)

    if request.user != room.host:
        return redirect('index')

    if request.method == "POST":
        room.delete()
        return redirect('index')
