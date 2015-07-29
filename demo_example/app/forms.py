from django.views.generic.edit import UpdateView
from django.forms.models import modelformset_factory

from knockout import forms as knockout_forms

from app import models


class PersonForm(knockout_forms.KnockoutForm):

    class Meta:
        model = models.Person
        fields = '__all__'


class FormsetUpdateView(UpdateView):
    can_delete = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'form' in context:
            formset = context.pop('form')
            context['formset'] = formset

        return context

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        return queryset

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if 'instance' in kwargs:
            queryset = kwargs.pop('instance')
            kwargs['queryset'] = queryset

        return kwargs

    def get_form_class(self):
        if self.form_class:
            return self.form_class

        form_class = modelformset_factory(self.model, fields='__all__',
                                          can_delete=self.can_delete)

        return form_class
