from django.db import models

# Create your models here.

class Command(models.Model):
    command_text = models.CharField(max_length=200)

class Response(models.Model):
    command = models.ForeignKey(Command, on_delete=models.CASCADE)
    response_text = models.CharField(max_length=200)
