from django.db import models

# Create your models here.
from apps.course.models import Course
from apps.myuser.models import UserProfile


class UserAsk(models.Model):
    '''
    用户咨询表
    '''
    name = models.CharField(max_length=20, verbose_name='名字')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    course_name = models.CharField(max_length=50, verbose_name='课程名')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户咨询表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseComment(models.Model):
    '''
    课程评论表
    '''
    user = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, verbose_name='评论用户')
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, verbose_name='课程')
    comment = models.CharField(max_length=200, verbose_name='评论内容')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    class Meta:
        verbose_name = '课程评论表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comment


class UserFavorite(models.Model):
    '''
    用户收藏表
    '''
    FAV_TYPE_CHOICE = (
        (1, '课程'),
        (2, '机构'),
        (3, '教师'),
    )

    user = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, verbose_name='收藏用户')
    fav_type = models.IntegerField(choices=FAV_TYPE_CHOICE, verbose_name='收藏类型')
    fav_id = models.IntegerField(default=1, verbose_name='收藏ID')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        verbose_name = '用户收藏表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fav_id


class UserMessage(models.Model):
    '''
    用户消息表
    '''
    # 当user=0，消息发给全体
    user = models.IntegerField(default=0, verbose_name='接收用户ID')
    message = models.CharField(max_length=500, verbose_name='消息内容')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='消息发出时间')

    class Meta:
        verbose_name = '用户消息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message


class UserCourse(models.Model):
    '''
    用户课程表
    '''
    user = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, verbose_name='用户')
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, verbose_name='课程')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户课程表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user
