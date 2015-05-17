from django.conf.urls import include, url
from django.contrib import admin

from app import views


urlpatterns = [
    url(r'^$', views.Index.as_view(), name="index"),
    url(r'^app/', include('app.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
