"""domino_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
# from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from dominoapi.models import *
from dominoapi.views import TaskLists, Tasks, Steps, TaskSteps, Users

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'taskLists', TaskLists, 'list')
# first argument = url route, second argument = name of viewset, third argument = view_name
router.register(r'tasks', Tasks, 'task')
router.register(r'steps', Steps, 'step')
router.register(r'tasksteps', TaskSteps, 'taskstep')
router.register(r'users', Users, 'user')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
