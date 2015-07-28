from knockout import forms as knockout_forms

from app import models


class PersonForm(knockout_forms.KnockoutForm):

    class Meta:
        model = models.Person
        fields = '__all__'
