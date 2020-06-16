"""View module for handling requests about tasksteps"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from dominoapi.models import Step, Task, TaskStep


class TaskStepSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for tasksteps

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = TaskStep
        url = serializers.HyperlinkedIdentityField(
            view_name='taskstep',
            lookup_field='id'
        )
        fields = ('id', 'task', 'step',)
        depth = 1

class TaskSteps(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for single taskstep

        Returns:
            Response -- JSON serialized taskstep instance
        """
        try:
            task = Task.objects.get(pk=pk)
            step = Step.objects.get(pk=pk)
            taskstep = TaskStep.objects.get(pk=pk)
            serializer = TaskStepSerializer(taskstep, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
            
    def list(self, request):
        """Handle GET requests to tasksteps resource

        Returns:
            Response -- JSON serialized list of tasksteps
        """
        tasksteps = TaskStep.objects.all()
        serializer = TaskStepSerializer(
            tasksteps,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)