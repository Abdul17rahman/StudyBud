from django.shortcuts import render, redirect
from .models import Room, Topic, User
from django.db.models import Q
# from .form import RoomForm

# Create your views here.

def index(request):
    
    topics = Topic.objects.all()

    q = request.GET.get('q', '').strip()

    if q:
        # Implement a Q lookup for different fields
        rooms = Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        ).order_by("-created")
    else:
        rooms = Room.objects.all().order_by("-created")

    return render(request, "index.html", {"rooms": rooms, "topics":topics})


def room(request, id):
    context = Room.objects.get(id=int(id))
    return render(request, "room.html", {"room":context})

def create(request):

    hosts = User.objects.all()
    topics = Topic.objects.all()

    if request.method == "POST":
        
        host_id = request.POST.get('host')
        topic_id = request.POST.get('topic')
        name = request.POST.get('name')
        description  = request.POST.get('desc')

        host = User.objects.get(id=host_id)
        topic = Topic.objects.get(id=topic_id)

        room = Room(host=host, topic=topic, name=name, description=description)
        room.save()

        return redirect('index')

    return render(request, "create.html", {
        "topics": topics,
        "hosts":hosts
    })

def update(request, id):

    room  = Room.objects.get(id=int(id))
    topics = Topic.objects.all()

    if request.method == "POST":
        
        topic_id = request.POST.get('topic')
        name = request.POST.get('name')
        description  = request.POST.get('desc')

        topic = Topic.objects.get(id=topic_id)

        room.topic = topic
        room.name = name
        room.description = description

        room.save()

        return redirect('room', id=room.id)

    return render(request, "update.html", {"room": room, "topics": topics})

def delete(request, id):
    
    room = Room.objects.get(id=id)

    if request.user != room.host:
        return redirect('index')
    
    if request.method == "POST":
        room.delete()
        return redirect('index')
    