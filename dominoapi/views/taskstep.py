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
            # task = Task.objects.get(pk=pk)
            # step = Step.objects.get(pk=pk)
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

    
    # def create(self, request):
        
    #     try:
    #         step = Step.objects.get(pk=request.data['step_id'])
            
    #         new_task_step = TaskStep()
    #         new_task_step.task_id = request.data['task_id']
    #         new_task_step.step_id = step.id
            
    #         new_task_step.save()

    #         serialize = TaskStepSerializer(new_order_product, context={'request': request}) 
    #     except:
    #         new_step = Step()
    #         new_step.name = request.data['step_name']
    #         new_step.description = request.data['step_description']
    #         new_step.is_complete = False
    #         new_step.importance = None
    #         new_step.save()

    #         new_task_step = TaskStep()
    #         new_task_step.task_id = request.data['task_id']
    #         new_task_step.step_id = new_step.id

    #         new_order_product.save()

    #         serialize = TaskStepSerializer(new_order_product, context={'request': request}) 

    #     return Response(serialize.data) 
    
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