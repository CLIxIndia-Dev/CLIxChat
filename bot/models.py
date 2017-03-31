from django.db import models

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