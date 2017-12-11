from django.conf.urls import url
from . import views

app_name = 'message'
urlpatterns = [
    url(r'^message/$', views.Hmessage, name='message'),
    url(r'^acm/$', views.HacMessage, name='acm'),
    url(r'^wam/$', views.HwaMessage, name='wam'),
]
