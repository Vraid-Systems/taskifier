from django.db import models

class Task(models.Model):
    owner = models.ForeignKey('TaskOwner', on_delete=models.CASCADE)
    source = models.TextField()
    dest = models.TextField()
    content = models.TextField()
    delay_seconds = models.IntegerField(default=0) # plenty for 50 years = 1.57 billion
    modified = models.DateTimeField(auto_now=True, auto_now_add=True)

class TaskOwner(models.Model):
    email = models.EmailField()
    key = models.CharField(max_length=255)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True)
