from django.urls import path, re_path
from restaurant import views

urlpatterns = [
    path('', views.index, name='home'),
    path('cats/<int:cat_id>/', views.categories, name='cats_id'),
    path('cats/<slug:cat_slug>/', views.categories_by_slug, name='cats'),
    path('archive/<year4:year>/', views.archive, name='archive'),
    path('add_feedback/', views.add_feedback, name='add_feedback'),
    path('about/', views.about, name='about'),
]
