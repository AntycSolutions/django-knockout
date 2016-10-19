from django.conf.urls import url
from django.conf import urls

from rest_framework import routers

from app import views, api


router = routers.DefaultRouter()
router.register(
    r'persons',
    api.PersonViewSet,
    'person'
)
router.register(
    r'tasks',
    api.TaskViewSet,
    'task'
)
router.register(
    r'shopping_lists',
    api.ShoppingViewSet,
    'shopping'
)

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='app_index'),
    url(r'^persons/$', views.Persons.as_view(), name='persons'),
    url(r'^persons_form/(?P<pk>\d+)/$',
        views.PersonsForm.as_view(),
        name='persons_form'),
    url(r'^persons_formset/$', views.PersonsFormset.as_view(),
        name='persons_formset'),
    url(r'^schedule/$', views.Schedule.as_view(), name='schedule'),
    url(r'^shopping/$', views.Shopping.as_view(), name='shopping'),
    url(r'^multiple_models/$',
        views.MultipleModels.as_view(),
        name='multiple_models'),

    urls.url(r'^api/', urls.include(router.urls)),
]
