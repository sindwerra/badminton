from django.db import models

from back_b_b import abs_models
from account import models as account_models


class Sites(abs_models.BaseModel):
    '''场地基本信息'''
    # 场地唯一标识符
    site_sign = models.CharField(max_length=128, blank=True, null=True, unique=True)
    # 标题
    title = models.CharField(max_length=128, blank=True, null=True)
    # 具体地点
    site = models.CharField(max_length=128, blank=True, null=True)
    # 活动区域（省市）
    zone = models.CharField(max_length=128, blank=True, null=True)
    # 球馆场地数量
    capacity = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'sites'


class Actions(abs_models.BaseModel):
    '''具体活动信息'''
    # 球馆
    site = models.ForeignKey(Sites, models.DO_NOTHING, blank=True, null=True)
    # 活动最大参与人数
    limit_number = models.IntegerField(default=6)
    # 活动创建者
    manager = models.ForeignKey(account_models.User, models.DO_NOTHING, blank=True, null=True)
    # 活动开始时间
    start_on = models.DateTimeField(blank=True, null=True)
    # 活动结束时间
    end_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'site_info'


class BookInfo(models.Model):
    '''用户的单个预约信息'''
    # 关联活动
    action = models.ForeignKey(Actions, models.DO_NOTHING, blank=True, null=True, related_name='current_bookings')
    # 报名用户
    user = models.ForeignKey(account_models.User, models.DO_NOTHING, blank=True, null=True, related_name='current_actions')
    # 报名人数
    booking_number = models.IntegerField(default=1)

    class Meta:
        db_table = 'book_info'