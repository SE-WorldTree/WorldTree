from django.conf.urls import url
from . import views

app_name = 'graph'
urlpatterns = [
    url(r'^tmp/$', views.tmp, name='tmp'),
    #url(r'^profile/$', views.Hprofile, name='profile'),
    url(r'^addv/$', views.HaddNode, name='addNode'),
    url(r'^newv/$', views.HnewNode, name='newNode'),
    url(r'^edit/$', views.HeditNode, name='edit'),
    url(r'^delv/$', views.HremoveNode, name='removeNode'),
    url(r'^adde/$', views.HaddEdge, name='addEdge'),
    url(r'^dele/$', views.HremoveEdge, name='removeEdge'),
    #url(r'^showgraph/$', views.showgraph, name='showgraph'),
    url(r'^tree/$', views.showgraph, name='tree'),
]
