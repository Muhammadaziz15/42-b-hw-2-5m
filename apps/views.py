from rest_framework import generics

from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all().order_by("-created_at")
    serializer_class = TaskSerializer


class TaskRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
