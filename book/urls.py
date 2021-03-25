from django.conf.urls import url, include
from django.contrib import admin

from book import views

urlpatterns = [
    # 管理员————发布新的场地信息  1
    url(r'^addsiteinfo/', views.add_siteinfo),
    # 管理员————查看所有的申请信息 1
    url(r'^allnewbook/', views.all_new_bookinfo),
    # 管理员————通过或拒绝一个申请 1
    url(r'^changebook/', views.change_bookinfo_status),
    # 管理员————查看所有自己发布的场地信息 1
    url(r'^allmysiteinfo/', views.get_all_my_siteinfo),

    # 用户————获取所有场地信息  1
    url(r'^allsiteinfo/', views.get_all_siteinfo),
    # 用户————获取所有未满的场地信息  1
    url(r'^allnotfullsiteinfo/', views.get_all_notfull_siteinfo),
    # 用户————查看某个场地的详细信息  1
    url(r'^getdetail/', views.get_siteinfo_getdetail),
    # 用户————查看自己预约过的场地信息  1
    url(r'^getmybooks/', views.get_my_bookinfo),
    # 用户————预约某个场地 1
    url(r'^booksiteinfo/', views.book_siteinfo),
    # 用户————按照参加次数进行排序
    url(r'^all_booked/', views.all_booked),
    # 用户————查看自己预约成功的总次数
    url(r'^allpass/', views.all_pass),
    # 用户————查看自己在某个场地预约成功的总次数
    url(r'^allpassbysite/', views.all_pass_bysite),
    # 用户————查看所以具体场地的历史发布信息次数
    url(r'^countbysite/', views.count_bysite),

    url(r'^action/(?P<record_id>\d+)/bookinfo/$', views.get_book_info_by_action),
]


