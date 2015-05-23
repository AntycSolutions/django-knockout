from django.conf.urls import url

from app import views


urlpatterns = [
    url(r'^$', views.Index.as_view(), name='app_index'),
    url(r'persons/$', views.Persons.as_view(), name='persons'),
    url(r'schedule/$', views.Schedule.as_view(), name='schedule'),
    url(r'shopping/$', views.Shopping.as_view(), name='shopping'),
]
