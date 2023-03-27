# common/urls.py
from django.urls import path
from django.contrib.auth import views as auth_view # INSTALLED_APPS에 기본으로 있음, 로그인 관련

# 현재 폴더에서 views.py를 가지고 오는데 그 이름이 common_view
from . import views as common_view

urlpatterns = [
    path('', common_view.index),
    path('login/', auth_view.LoginView.as_view(template_name = 'common/login.html')),
    path('logout/', auth_view.LogoutView.as_view()),
    path('singup/', common_view.signup),
]