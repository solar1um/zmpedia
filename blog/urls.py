from django.urls import path
from .views import main_page, create_post, category_posts, search, post_detail, post_update, post_delete, \
    user_posts, rate_post

urlpatterns = [
    path('rate/<int:pk>/<int:rate>/', rate_post, name='rate'),
    path('post-delete/<int:pk>/', post_delete, name='post_delete'),
    path('post-update/<int:pk>/', post_update, name='post_update'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('category/<int:pk>/', category_posts, name='category_posts'),
    path('my-posts/', user_posts, name='my_posts'),
    path('create-post', create_post, name='create_post'),
    path('search/', search, name='search'),
    path('', main_page, name='main_page'),
]
