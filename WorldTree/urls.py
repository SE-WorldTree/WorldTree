"""WorldTree URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
import userManagement.views as um_views
import relation.views as rel_views
from django.conf import settings
import graphGeneration.views as gg_views
import graphGeneration.templates as gg_tmp


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', um_views.login, name='login'),
    url(r'^login/$', um_views.login, name='login'),
    url(r'^register/$', um_views.register, name='register'),
    url(r'^index/$', um_views.index, name='index'),
    url(r'^logout/$', um_views.logout, name='logout'),
    url(r'^addv/$', rel_views.addVertex, name='addv'),
    url(r'^adde/$', rel_views.addEdge, name='adde'),
    url(r'^qid/$', rel_views.queryID, name='qid'),
    url(r'^qe/$', rel_views.queryEdge, name='qe'),
    url(r'^vertexDetail/$', rel_views.vertexDetail, name='vertexDetail'), # for graph generation
    url(r'^gao/$', rel_views.main, name='gao'), # temp
    url(r'^gg/', gg_views.gg, name='GG'),
    url(r'^testData', gg_views.testData, name='GGWP'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

