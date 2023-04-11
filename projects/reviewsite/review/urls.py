from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('add_movie/', views.add_movie, name = 'add_movie'),
    path('review_movie/<int:id>', views.review_movie, name = 'review_movie'),
    path('update_movie/<int:id>', views.update_movie, name = 'update_movie'),
    path('delete_movie/<int:id>', views.delete_movie, name = 'delete_movie'),
    path('review_movie/<int:id>/reply/', views.reply, name = 'reply'),
    path('recently/', views.recently, name = 'recently'),
]