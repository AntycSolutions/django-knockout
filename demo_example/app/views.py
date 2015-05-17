from django.views.generic import TemplateView

from app import models


class Index(TemplateView):
    template_name = "app/index.html"


class Persons(TemplateView):
    template_name = "app/persons.html"

    def get_context_data(self, **kwargs):
        context = super(Persons, self).get_context_data(**kwargs)

        persons = models.Person.objects.all()
        context['persons'] = persons

        return context


class Schedule(TemplateView):
    template_name = "app/schedule.html"

    def get_context_data(self, **kwargs):
        context = super(Schedule, self).get_context_data(**kwargs)

        schedule = models.Task.objects.all()
        context['schedule'] = schedule

        return context
