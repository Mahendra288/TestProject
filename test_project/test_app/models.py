import datetime
import factory
from django.db import models, transaction


# Create your models here.

def validate_name(name):
    if not len(name) >= 2:
        raise Exception


class Author(models.Model):
    name = models.CharField(max_length=100)


class Book(models.Model):
    name = models.CharField(max_length=40, validators=[validate_name])
    price = models.PositiveIntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
