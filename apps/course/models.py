from django.db import models

# Create your models here.
from apps.organization.models import CourseOrg, Teacher


class Course(models.Model):
    '''
    课程信息表
    '''
    DEGREE_CHOICE = (
        ('cj', '初级'),
        ('zj', '中级'),
        ('gj', '高级'),
    )

    CATEGORY_CHOICE = (
        (0, '后端开发'),
        (1, 'Web前端开发'),
        (2, '数据库设计'),
    )

    courseorg = models.ForeignKey(CourseOrg, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='课程机构')
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='课程教师')
    name = models.CharField(max_length=50, verbose_name='课程名')
    desc = models.CharField(max_length=200, verbose_name='课程简述')
    detail = models.TextField(verbose_name='课程详情')
    degree = models.CharField(max_length=4, choices=DEGREE_CHOICE, verbose_name='难度级别')
    learn_time = models.IntegerField(default=0, verbose_name='学习时长(分)')
    students = models.IntegerField(default=0, verbose_name='学生人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m', max_length=100, null=True, blank=True, verbose_name='封面')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    category = models.SmallIntegerField(choices=CATEGORY_CHOICE, default=0)
    tag = models.CharField(max_length=50, null=True, blank=True, verbose_name='课程标签')   # 可用于相关课程推荐
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程信息表'
        verbose_name_plural = verbose_name

    def get_usercourse_set(self):
        """
        该课程的学习用户
        :return:
        """
        return self.usercourse_set.only('user').distinct()[:5]

    def __str__(self):
        return self.name


class Section(models.Model):
    '''
    章节表
    '''
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, verbose_name='课程外键')
    name = models.CharField(max_length=10, verbose_name='章节名')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(models.Model):
    '''
    视频表
    '''
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING, verbose_name='章节外键')
    name = models.CharField(max_length=50, verbose_name='视频名')
    url = models.URLField(default='', verbose_name='视频访问地址')
    howlong = models.IntegerField(default=0, verbose_name='视频时长（分）')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    '''
    课程下载资源表
    '''
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, verbose_name='课程外键')
    name = models.CharField(max_length=50, verbose_name='课程资源名')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    download = models.FileField(upload_to='course/resource/%Y/%m', max_length=100, verbose_name='下载地址')

    class Meta:
        verbose_name = '课程下载资源表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
