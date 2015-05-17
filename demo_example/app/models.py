from django.db import models


class Person(models.Model):
    first_name = models.CharField("First Name", max_length=64)
    last_name = models.CharField("Last Name", max_length=64)


class Day(models.Model):
    day = models.DateField("Day")


class Task(models.Model):
    task = models.TextField("Task")
    day = models.ForeignKey(Day)
