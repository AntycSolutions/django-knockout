from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse

from app import forms
from app import models


class Index(TemplateView):
    template_name = "app/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        person = models.Person.objects.first()
        context['person'] = person

        return context


class Persons(TemplateView):
    template_name = "app/persons.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        persons = models.Person.objects.all()
        context['persons'] = persons

        person_class = models.Person
        context['person_class'] = person_class

        return context


class PersonsForm(UpdateView):
    template_name = "app/persons_form.html"
    model = models.Person
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['PersonClass'] = models.Person

        context['knockout_form'] = forms.PersonForm(instance=self.object)

        return context

    def get_success_url(self):
        self.success_url = reverse('persons_form',
                                   kwargs={'pk': self.object.pk})

        return self.success_url


class PersonsFormset(forms.FormsetUpdateView):
    template_name = "app/persons_formset.html"
    model = models.Person

    def get_success_url(self):
        self.success_url = reverse('persons_formset')

        return self.success_url


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
            'items', 'items__description'
        )
        context['shopping_lists'] = shopping_lists

        context['item_class'] = models.Item

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
            'items', 'items__description'
        )
        context['shopping_lists'] = shopping_lists

        return context
