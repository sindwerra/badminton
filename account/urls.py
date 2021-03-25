from django.conf.urls import url, include
from django.contrib import admin

from account import views

urlpatterns = [
    # 注册新的用户
    url(r'^register/', views.register),
    # 获取用户的个人资料
    url(r'^change_profile/', views.change_authority),
    # 更改用户的管理员权限
    url(r'^get_user_profile/', views.get_user_profile),


]


