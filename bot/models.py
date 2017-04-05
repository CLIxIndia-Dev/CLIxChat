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


class Node(MPTTModel):
    name = models.SlugField(max_length=200, unique=True)
    button_text = models.CharField(max_length=200)
    inline_text = models.CharField(max_length=200)
    # command_text = models.SlugField(max_length=100, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    def __str__(self):
        return self.name

    # class MPTTMeta:
    #     order_insertion_by = ['name']
#
# class Session(models.Model):
#     unit = models.TreeForeignKey(Unit, on_delete=models.CASCADE)
#     session_text = models.SlugField(max_length=100)
#     def __str__(self):
#         return self.session_text
#
# class Activity(models.Model):
#     session = models.TreeForeignKey(Session, on_delete=models.CASCADE)
#     activity_text = models.SlugField(max_length=100)
#     def __str__(self):
#         return self.activity_text