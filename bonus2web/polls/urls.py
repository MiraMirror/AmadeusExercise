from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # ex: /polls/5/
    url(r'^(?P<n>[0-9]+)/$', views.detail, name='detail'),
]