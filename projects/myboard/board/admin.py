from django.contrib import admin
from .models import Board

# Register your models here.

# 내가 만든 커스텀 모델 등록
admin.site.register(Board)