from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class UserProfile(AbstractUser):
    '''
    用户信息表，继承了内置抽象表AbstractUser
    '''
    GENDER_CHOICE = (
        ('male', '男'),
        ('female', '女'),
    )
    nick_name = models.CharField(max_length=20, verbose_name='昵称')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    gender = models.CharField(max_length=5, choices=GENDER_CHOICE, default=GENDER_CHOICE[0][0], verbose_name='性别')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='地址')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
    image = models.ImageField(max_length=100, upload_to='headimg/%Y-%m-%d', default='headimg/default.jpg',
                              verbose_name='上传图片的地址')

    class Meta:
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s(%s)' % (self.username, self.nick_name)
