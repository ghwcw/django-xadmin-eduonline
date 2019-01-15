from django.db import models


# Create your models here.


class CityDict(models.Model):
    '''
    城市字典表
    '''
    name = models.CharField(max_length=10, verbose_name='城市名')
    desc = models.CharField(max_length=200, verbose_name='城市详细描述')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '城市字典表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    '''
    教育机构表
    '''
    CATEGORY_CHOICE = (
        ('pxjg', '培训机构'),
        ('gx', '高效'),
        ('gr', '个人'),
    )

    name = models.CharField(max_length=50, verbose_name='机构名称')
    desc = models.TextField(verbose_name='机构描述')
    category = models.CharField(max_length=10, choices=(CATEGORY_CHOICE), default='pxjg', verbose_name='机构分类')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name='logo', default='org/default-org.jpg', null=True,
                              blank=True)
    city = models.ForeignKey(CityDict, on_delete=models.DO_NOTHING, verbose_name='机构所在城市')
    students = models.IntegerField(verbose_name='学生人数', default=0)
    courses = models.IntegerField(verbose_name='课程数', default=0)
    address = models.CharField(max_length=100, verbose_name='机构地址')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '教育机构表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_course_set(self):
        return self.course_set.order_by('-fav_nums').all()[:3]


class Teacher(models.Model):
    '''
    教师信息表
    '''
    org = models.ForeignKey(CourseOrg, verbose_name='所属机构')
    name = models.CharField(max_length=20, verbose_name='名称')
    age = models.SmallIntegerField(null=True, blank=True, verbose_name='年龄')
    speciality = models.CharField(max_length=200, null=True, blank=True, verbose_name='特长')
    work_year = models.SmallIntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='所在公司')
    work_position = models.CharField(max_length=20, verbose_name='工作职位')
    image = models.ImageField(upload_to='teacher/%Y/%m', max_length=100, verbose_name='头像', null=True, blank=True,
                              default='image/default.jpg')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '教师信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
