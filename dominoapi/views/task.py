"""View module for handling requests about tasks"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from dominoapi.models import Task, List, TaskStep, Step
from django.contrib.auth.models import User


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
            # task_list = List.objects.get(pk=pk)
            # user = User.objects.get(pk=pk)
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
        if task_list is not None:
            tasks = Task.objects.filter(user=request.auth.user, task_list=task_list)
        else:
            tasks = Task.objects.filter(user=request.auth.user)
        
        serializer = TaskSerializer(
            tasks,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


    def create(self, request):

        task_list = List.objects.get(pk=request.data["task_list_id"])
        user = request.auth.user

        new_task = Task()
        new_task.user = user
        new_task.task_list = task_list
        new_task.name = request.data["name"] 
        new_task.importance = None
        new_task.recurring = None
        new_task.is_complete = False
        if request.data["description"] == "null":
            new_task.description = None
        else:
            new_task.description = request.data["description"]
        
        new_task.save()

        serializer = TaskSerializer(
            new_task, context={'request': request}
        )

        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for an individual task
        Returns:
            Response -- Empty body with 204 status code
        """
        complete = self.request.query_params.get('complete', None)

        if complete is not None:
            task = Task.objects.get(pk=pk)
            task.is_complete = request.data["is_complete"]
        else:
            task_list = List.objects.get(pk=request.data["task_list_id"])
            task = Task.objects.get(pk=pk)
            task.name = request.data["name"]
            task.description = request.data["description"]
            task.task_list = task_list
        task.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single task
        Returns:
            Response -- 200, 404, or 500 status code
        """

        try:
            task = Task.objects.get(pk=pk)
            task.delete()

            steps = Step.objects.all()
            task_steps = TaskStep.objects.all()
            step_ids = set()
            task_step_ids = set()
            for step in steps:
                step_ids.add(step.id)
            for task_step in task_steps:
                task_step_ids.add(task_step.step.id)
            print("stepIds", step_ids)
            print("taskStepIds:", task_step_ids)
            for step_id in step_ids:
                if step_id not in task_step_ids:
                    step_to_delete = Step.objects.get(pk=step_id)
                    step_to_delete.delete()
                    # print("stepToDelete:", step_to_delete)
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Task.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
