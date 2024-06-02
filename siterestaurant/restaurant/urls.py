from django.urls import path, re_path
from restaurant import views
from restaurant.templatetags import restaurant_tags
from restaurant.views import RestaurantCategory

# from show_category import restaurant_tags

urlpatterns = [
    path('', views.RestaurantHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('look/', views.look, name='look'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', RestaurantCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
    path('addPoll/', views.AddPoll.as_view(), name='addPoll'),
    path('edit/<slug:slug>/', views.UpdatePoll.as_view(), name='edit_page'),
    path('delete/<slug:slug>/', views.DeletePoll.as_view(), name='delete_page'),


]
