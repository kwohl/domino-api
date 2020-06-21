"""View module for handling requests about steps"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from dominoapi.models import Step


class StepSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for steps

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Step
        url = serializers.HyperlinkedIdentityField(
            view_name='step',
            lookup_field='id'
        )
        fields = ('id', 'name', 'description', 'is_complete',)

class Steps(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for single step

        Returns:
            Response -- JSON serialized step instance
        """
        try:
            step = Step.objects.get(pk=pk)
            serializer = StepSerializer(step, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
            
    def list(self, request):
        """Handle GET requests to steps resource

        Returns:
            Response -- JSON serialized list of steps
        """
        steps = Step.objects.all()
        serializer = StepSerializer(
            steps,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def create(self, request):

        new_step = Step()
        new_step.name = request.data["name"] 
        new_step.importance = None
        new_step.is_complete = False
        if request.data["description"] == "null":
            new_step.description = None
        else:
            new_step.description = request.data["description"]
        
        new_step.save()

        serializer = StepSerializer(
            new_step, context={'request': request}
        )

        return Response(serializer.data)