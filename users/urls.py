from django.conf.urls import url

from users.views import ActiveUserView
from . import views

app_name = 'users'
urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^balabala/', views.rejson, name='rejson'),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active")
]
