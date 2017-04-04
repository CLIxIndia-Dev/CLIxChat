# from django.db import models
import from treebeard import models
# Create your models here.

class Command(models.Model):
    command_text = models.SlugField(max_length=100, unique=True)
    def __str__(self):
        return self.command_text

class Response(models.Model):
    command = models.ForeignKey(Command, on_delete=models.CASCADE)
    response_text = models.CharField(max_length=200)
    def __str__(self):
        return self.response_text


class Unit(models.Node):
    unit_text = models.SlugField(max_length=100)
    def __str__(self):
        return self.unit_text

class Session(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    session_text = models.SlugField(max_length=100)
    def __str__(self):
        return self.session_text

class Activity(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    activity_text = models.SlugField(max_length=100)
    def __str__(self):
        return self.activity_text