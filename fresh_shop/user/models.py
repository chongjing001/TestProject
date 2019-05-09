from django.db import models

# Create your models here.


# 用户模块:

class User(models.Model):
    """
     用户表
    """
    username = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="姓名")
    password = models.CharField(max_length=255, verbose_name="密码")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    GENDER = (
        ("male", u"男"),
        ("female", "女")
    )
    gender = models.CharField(max_length=6, choices=GENDER, default="female",
                              verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")

    class Meta:
        db_table = 'f_user'


class UserAddress(models.Model):
    """
    收货地址表
    """
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    province = models.CharField(max_length=100, default='', verbose_name='省份')
    city = models.CharField(max_length=100, default='', verbose_name='城市')
    district = models.CharField(max_length=100, default='', verbose_name='区域')
    address = models.CharField(max_length=100, default='', verbose_name='详细地址')
    signer_name = models.CharField(max_length=20, default='', verbose_name='签收人')
    signer_mobile = models.CharField(max_length=11, default='', verbose_name='电话')
    signer_postcode = models.CharField(max_length=11, default='', verbose_name='邮编')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        db_table = 'f_user_address'







