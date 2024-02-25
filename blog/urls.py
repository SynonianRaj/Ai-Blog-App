from django.urls import path,include
from . import views as my_view

urlpatterns = [
    path("", my_view.home, name="blog-home" ),
    path('about/', my_view.about, name='blog-about'),
    path('contact/', my_view.contact, name='blog-contact'),
    path('user/sign-up',my_view.register_page, name='sign-up-user'),
    path('user/sign-in',my_view.login_page, name='sign-in-user'),
    path('user/log-out',my_view.logout_page, name='sign-out-user'),
    path('article/<int:id>/<str:title>',my_view.articles, name='article-page'),
    path('postliked', my_view.post_liked, name='postliked'),
    


]