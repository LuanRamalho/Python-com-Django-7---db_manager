from django.contrib.auth.models import User
from django.db import models

class Database(models.Model):
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Table(models.Model):
    name = models.CharField(max_length=100)
    database = models.ForeignKey(Database, on_delete=models.CASCADE)

class Column(models.Model):
    name = models.CharField(max_length=100)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    data_type = models.CharField(max_length=50)

class Row(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    data = models.JSONField()
