from django.conf.urls import url

from app import views


urlpatterns = [
    url(r'^$', views.Index.as_view(), name='app_index'),
    url(r'persons/$', views.Persons.as_view(), name='persons'),
    url(r'persons_form/(?P<pk>\d+)/$', views.PersonsForm.as_view(),
        name='persons_form'),
    url(r'persons_formset/$', views.PersonsFormset.as_view(),
        name='persons_formset'),
    url(r'schedule/$', views.Schedule.as_view(), name='schedule'),
    url(r'shopping/$', views.Shopping.as_view(), name='shopping'),
    url(r'multiple_models/$', views.MultipleModels.as_view(),
        name='multiple_models'),
]
