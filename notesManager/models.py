
from django.db import models
from django.contrib.auth.models import User


class NoteGroup(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(NoteGroup, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class Remainder(models.Model):
    class Priority(models.IntegerChoices):
        HIGH = 3
        MEDIUM = 2
        LOW = 1
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    date = models.DateField()
    hour = models.TimeField()
    priority = models.IntegerField(choices=Priority.choices)
    done = models.BooleanField(default=False)

