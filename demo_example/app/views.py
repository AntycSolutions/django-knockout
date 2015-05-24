from django.views.generic import TemplateView

from app import models


class Index(TemplateView):
    template_name = "app/index.html"


class Persons(TemplateView):
    template_name = "app/persons.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        persons = models.Person.objects.all()
        context['persons'] = persons

        return context


class Schedule(TemplateView):
    template_name = "app/schedule.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        schedule = models.Task.objects.all().select_related(
            'day', 'reminder', 'reminder__reminder_type'
        )
        context['schedule'] = schedule

        return context


class Shopping(TemplateView):
    template_name = "app/shopping.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        shopping_lists = models.Shopping.objects.all().prefetch_related(
            'items'
        )
        context['shopping_lists'] = shopping_lists

        return context


class MultipleModels(TemplateView):
    template_name = "app/multiple_models.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        persons = models.Person.objects.all()
        context['persons'] = persons

        schedule = models.Task.objects.all().select_related(
            'day', 'reminder', 'reminder__reminder_type'
        )
        context['schedule'] = schedule

        shopping_lists = models.Shopping.objects.all().prefetch_related(
            'items'
        )
        context['shopping_lists'] = shopping_lists

        return context
