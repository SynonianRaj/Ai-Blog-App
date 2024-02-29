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
    # path("get-post/", my_view.get_posts, name='get-post'),
    path('load-more-posts/',my_view.load_more_posts, name = 'load-more-posts'),
    path('search', my_view.search_page, name='search-page'),
    
    


]