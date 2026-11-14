from django.db import models

class Task(models.Model):
    title =       models.CharField(max_length=200)
    description = models.TextField()
    status =      models.BooleanField(default=False)
    priority =    models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
