from django.urls import path
from . import views

# 다른 앱에서 같은 URL별칭 중복 예방, 네임스페이스
app_name = 'board'

urlpatterns = [
    # .../board
    path('', views.index, name = 'index'),
    # 글읽기 주소
    path('<int:id>/', views.read, name = 'detail'),
    # 글쓰기 주소
    path('write/', views.write, name = 'write'),
    # 수정 주소
    path('<int:id>/update/', views.update, name = 'update'),
    # 삭제 주소
    path('<int:id>/delete/', views.delete, name = 'delete'),
    # 댓글쓰기 주소
    path('<int:id>/write_reply', views.write_reply, name = 'write_reply'),

    # AJAX
    path('callAjax/', views.call_ajax),
    # AJAX 댓글 목록
    path('load_reply/', views.load_reply),
    # 댓글삭제 주소(id : 글번호, rid : 댓글번호)
    path('delete_reply/', views.delete_reply),
    # 댓글 수정
    path('update_reply/', views.update_reply),
    # 댓글 쓰기
    # path('write_reply/', views.write_reply),
]
