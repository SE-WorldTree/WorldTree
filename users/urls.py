from django.conf.urls import url

from users.views import ActiveUserView
from . import views

app_name = 'users'
urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^balabala/', views.rejson, name='rejson'),
    url(r'^relation/', views.uuuu, name='relation'),
    url(r'^profile/', views.nnnn, name='profile'),
    url(r'^message/', views.message, name='message'),
    url(r'^about/', views.about, name='about'),
    url(r'^hhhh/', views.hhhh, name='hhhh'),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active")
]
