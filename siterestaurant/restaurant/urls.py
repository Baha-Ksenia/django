from django.urls import path, re_path
from restaurant import views
from restaurant.templatetags import restaurant_tags

# from show_category import restaurant_tags

urlpatterns = [
    path('', views.index, name='home'),
    path('add/', views.addPoll, name='addPoll'),
    path('about/', views.about, name='about'),
    path('look/', views.look, name='look'),
    path('login/', views.login, name='login'),
    # path('post/<int:post_id>/', views.show_post, name='post'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
]
