from django.urls import path

from .views import ItemView, item_detail_api
from . import views
from rest_framework import permissions
from blog import views

handler404 = views.error_404

  
urlpatterns = [
   path('items/', views.home, name='home'),
   path('items/<int:id>/', views.details, name='item-detail'),
   path('author_review/<str:slug>/', views.author_review, name='author-review'),
   
   # path('api/items-api/', ItemView.as_view(),name='all_items_api'),
   path('api/', ItemView.as_view(), name='list-api'),
   path('api/<int:pk>/', item_detail_api.as_view(), name='details'),
   
]

