from os import name
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_user, name="login"),
    path('signup', views.signup_user, name="signup"),
    path('share', views.share, name='share'),
    path('logout', views.logout_user, name='logout'),
    path('my-posts', views.my_posts, name='my-posts'),
    path('edit-post/<str:id>', views.edit_post, name='edit-post'),
    path('delete-post/<str:id>', views.delete_post, name='delete-post'),
    path('search', views.search, name='search'),
]
