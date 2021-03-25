from django.db import models

class User(models.Model):
    '''用户表'''
    #昵称
    nickname = models.CharField(verbose_name=u'昵称', max_length=50, blank=True)
    #头像
    user_avatarurl = models.CharField(verbose_name=u'avatar',max_length=128)
    #用户id
    user_id = models.CharField(verbose_name=u'user_id',max_length=128, unique=True)
    #是否是管理员 0表示不是 1表示是
    is_manager = models.CharField(max_length=10,default='0')

    def __str__(self):
        return self.nickname


from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
