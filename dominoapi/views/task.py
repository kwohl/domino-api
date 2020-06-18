"""View module for handling requests about tasks"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from dominoapi.models import Task, List
from django.contrib.auth.models import User
from django.contrib.auth import get_user


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for tasks

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Task
        url = serializers.HyperlinkedIdentityField(
            view_name='task',
            lookup_field='id'
        )
        fields = ('id', 'name', 'description', 'is_complete', 'task_list', 'user')
        depth = 1

class Tasks(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for single task

        Returns:
            Response -- JSON serialized task instance
        """
        try:
            task_list = List.objects.get(pk=pk)
            user = User.objects.get(pk=pk)
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
            
    def list(self, request):
        """Handle GET requests to tasks resource

        Returns:
            Response -- JSON serialized list of tasks
        """
        task_list = self.request.query_params.get('list', None)
        tasks = Task.objects.filter(user=request.auth.user, task_list=task_list)
        serializer = TaskSerializer(
            tasks,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)