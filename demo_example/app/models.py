from django.db import models


class Person(models.Model):
    first_name = models.CharField("First Name", max_length=64)
    last_name = models.CharField("Last Name", max_length=64)


class Day(models.Model):
    day = models.DateField("Day")


class ReminderType(models.Model):
    reminder_type = models.CharField("Reminder", max_length=32)


class Reminder(models.Model):
    reminder = models.CharField("Reminder", max_length=32)
    reminder_type = models.ForeignKey(ReminderType)


class Task(models.Model):
    task = models.TextField("Task")
    day = models.ForeignKey(Day)
    reminder = models.ForeignKey(Reminder, blank=True, null=True)


class Description(models.Model):
    description = models.TextField("Description")


class Item(models.Model):
    name = models.CharField("Name", max_length=64)
    description = models.ForeignKey(Description, blank=True, null=True)


class Shopping(models.Model):
    name = models.CharField("Name", max_length=32)
    items = models.ManyToManyField(Item)
