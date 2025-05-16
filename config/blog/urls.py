from django.urls import path
from . import views


urlpatterns = [
    # READ
    path('', views.home, name='home'),
    # DETAIL READ
    path('blog/<int:blog_id>', views.detail, name='detail'),
    # CREATE
    path('blog/create', views.create, name='create'),
    path('<int:blog_id>/update/', views.update, name='update'), # 수정하는 함수와 연결
    path('<int:blog_id>/delete/', views.delete, name='delete'), # 삭제하는 함수와 연결
]