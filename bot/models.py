from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# class Command(models.Model):
#     command_text = models.SlugField(max_length=100, unique=True)
#     def __str__(self):
#         return self.command_text
#
# class Response(models.Model):
#     command = models.ForeignKey(Command, on_delete=models.CASCADE)
#     response_text = models.CharField(max_length=200)
#     def __str__(self):
#         return self.response_text


# class Unit(models.Model):
#     unit_text = models.SlugField(max_length=100)
#     def __str__(self):
#         return self.unit_text


class Element(MPTTModel):
    name = models.CharField(max_length=42, blank=True)
    # default button response = nav back
    message_text = models.TextField(blank=True)

    # command : the name of the button above it
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    def __str__(self):
        return self.name

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    last_node = models.ForeignKey(Element, null=True)
    last_visit = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)