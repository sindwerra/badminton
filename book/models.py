from django.db import models


class SiteInfo(models.Model):
    '''发布的场地信息'''
    # 单个实体的标识符
    siteinfo_sign = models.CharField(max_length=128)
    # 标题
    title_book = models.CharField(max_length=128)
    # 时间
    time_book = models.CharField(max_length=128)
    # 具体地点
    site_book = models.CharField(max_length=128)
    # 活动区域（省市）
    zone_book = models.CharField(max_length=128)
    # 支付方式
    payment_method = models.CharField(max_length=128)
    # 限制人数
    limit_number = models.IntegerField()
    # 剩余名额
    remaining_places = models.IntegerField()
    # 管理员的id
    manager_id = models.CharField(max_length=128)

class BookInfo(models.Model):
    '''用户的单个预约信息'''
    # 单个实体的标识符
    bookinfo_sign = models.CharField(max_length=128)
    # 所预约的预约信息的单个实体的标识符
    siteinfo_sign = models.CharField(max_length=128)
    # 用户昵称
    user_nickname = models.CharField(max_length=128)
    # 用户id
    user_id = models.CharField(max_length=128)
    # 用户头像url
    user_avatar = models.CharField(max_length=128)
    # 状态：1表示在申请中，2表示已通过，3表示被拒绝
    bookinfo_status = models.CharField(max_length=2)
