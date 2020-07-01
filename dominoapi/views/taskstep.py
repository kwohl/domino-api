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
        task = self.request.query_params.get('task', None)
        tasksteps = TaskStep.objects.filter(task=task)
        serializer = TaskStepSerializer(
            tasksteps,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def create(self, request):
        task = Task.objects.get(pk=request.data["task_id"])
        step = Step.objects.get(pk=request.data["step_id"])

        new_task_step = TaskStep()
        new_task_step.task = task 
        new_task_step.step = step
        
        new_task_step.save()

        serializer = TaskStepSerializer(
            new_task_step, context={'request': request}
        )

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single taskStep
        Returns:
            Response -- 200, 404, or 500 status code 
        """

        try:
            task_step = TaskStep.objects.get(pk=pk)
            step = Step.objects.get(pk=task_step.step.id)
            
            task_step.delete()

            task_step_step_ids = set()
            task_steps = TaskStep.objects.filter(step=step)
            
            for task_step in task_steps:
                task_step_step_ids.add(task_step.step.id)

            if step.id not in task_step_step_ids:
                step.delete()   

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Step.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
