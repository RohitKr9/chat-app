"""
URL configuration for ChatApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import chatApp, chatAppRoom, chatHome
from accounts.views import signup, login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat-app/', chatApp, name='app_landing'),
    path('chat-room/<int:userid>/', chatAppRoom, name='chatroom'),
    path('account/signup/', signup, name = 'signup'),
    path('account/login/', login, name = 'login'),
    path('chat-home/', chatHome, name="chat_home")
]
