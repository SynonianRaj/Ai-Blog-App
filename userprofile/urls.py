from django.urls import path
from . import views as user_views
from django.views.generic.base import RedirectView

app_name = 'userprofile'
urlpatterns = [

    path('profile', user_views.user_profile, name='user-profile-page'),
    path('', RedirectView.as_view(url='profile', permanent=False), name='user-profile-page'),
]