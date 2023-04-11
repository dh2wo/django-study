from django.urls import path
from . import views

app_name = 'item'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('addItem/', views.addItem, name = 'addItem'),\

    path('listItem/', views.listItem, name = 'listItem'),
    path('<int:id>/updateItem/', views.updateItem, name = 'updateItem'),
    path('deleteItem/', views.deleteItem, name = 'deleteItem'),
    path('searchItem/', views.searchItem, name = 'searchItem'),

    path('orderItem/', views.orderItem, name = 'orderItem'),
    path('orderList/', views.orderList, name = 'orderList'),
]

