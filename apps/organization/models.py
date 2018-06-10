from django.db import models


# Create your models here.

class CityDict(models.Model):
    '''
    城市字典表
    '''
    name = models.CharField(max_length=10, verbose_name='城市名')
    desc = models.CharField(max_length=200, verbose_name='机构描述')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '城市字典表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    '''
    课程机构表
    '''
    name = models.CharField(max_length=50, verbose_name='机构名称')
    desc = models.TextField(verbose_name='机构描述')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name='封面')
    city = models.ForeignKey(CityDict, on_delete=models.DO_NOTHING, verbose_name='机构所在城市')
    address = models.CharField(max_length=100, verbose_name='机构地址')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程机构表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(models.Model):
    '''
    教师信息表
    '''
    org = models.ForeignKey(CourseOrg, verbose_name='所属机构')
    name = models.CharField(max_length=20, verbose_name='名称')
    work_year = models.SmallIntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='所在公司')
    work_position = models.CharField(max_length=20, verbose_name='工作职位')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '教师信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
