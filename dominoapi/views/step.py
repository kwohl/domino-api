"""View module for handling requests about steps"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from dominoapi.models import Step, TaskStep


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

        # new_task_step = TaskStep()
        # new_task_step.step_id = new_step.id
        # new_task_step.task_id = request.data["task_id"]

        serializer = StepSerializer(
            new_step, context={'request': request}
        )

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single step
        Returns:
            Response -- 200, 404, or 500 status code 
        """

        try:
            step = Step.objects.get(pk=pk)
            step.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Step.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for an individual step
        Returns:
            Response -- Empty body with 204 status code
        """
        complete = self.request.query_params.get('complete', None)

        if complete is not None:
            step = Step.objects.get(pk=pk)
            step.is_complete = request.data["is_complete"]
        else:
            step = Step.objects.get(pk=pk)
            step.name = request.data["name"]
            step.description = request.data["description"]

        step.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
