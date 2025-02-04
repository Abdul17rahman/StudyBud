from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('room/<int:id>', views.room, name="room"),
    path('create/', views.create, name="create-room"),
    path('update/<int:id>', views.update, name="update-room"),
    path('delete/<int:id>', views.delete, name="delete"),
    path("login", views.login_page, name="login_page"),
    path("logout", views.logout_page, name="logout_page"),
    path("register", views.register, name="register")
]