from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid


# Create your models here.
class TodoLists(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tasks = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tasks
    
    @property
    def get_delete_url(self):
        return reverse('todo_delete', kwargs={'id': self.id})