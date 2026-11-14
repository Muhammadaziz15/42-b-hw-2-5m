from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    title =       serializers.CharField(max_length=200, allow_blank=False)
    description = serializers.CharField(min_length=10)
    priority =    serializers.IntegerField(min_value=1, max_value=5, default=1)

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ("id", "created_at")
