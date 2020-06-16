"""View module for handling requests about lists"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from dominoapi.models import List


class TaskListSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for lists

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = List
        url = serializers.HyperlinkedIdentityField(
            # view_name is connected to model name
            view_name='list',
            lookup_field='id'
        )
        fields = ('id', 'name', 'description')


class TaskLists(ViewSet):
    """Task Lists (categories) for Domino"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single list

        Returns:
            Response -- JSON serialized list instance
        """
        try:
            taskList = List.objects.get(pk=pk)
            serializer = TaskListSerializer(taskList, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
            
    def list(self, request):
        """Handle GET requests to lists resource

        Returns:
            Response -- JSON serialized list of task lists
        """
        taskLists = List.objects.all()
        serializer = TaskListSerializer(
            taskLists,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)