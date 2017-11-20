from django.conf.urls import url
from . import views

app_name = 'graph'
urlpatterns = [
    url(r'^tmp/$', views.tmp, name='tmp'),
    url(r'^profile/(?P<id>.+)/$', views.Hprofile, name='profile'),
    url(r'^addv/$', views.HaddNode, name='addNode'),
    url(r'^edit/(?P<id>.+)/$', views.HeditNode, name='edit'),
    url(r'^delv/(?P<id>.+)/$', views.HremoveNode, name='removeNode'),
    url(r'^adde/$', views.HaddEdge, name='addEdge'),
]
