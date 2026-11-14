from django.urls import path

from .views import TaskListCreateView, TaskRetrieveDestroyView

urlpatterns = [
    path("tasks/", TaskListCreateView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskRetrieveDestroyView.as_view(), name="task-detail"),
]
