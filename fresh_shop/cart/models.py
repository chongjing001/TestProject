from django.db import models

# Create your models here.


# 购物车模型：
from goods.models import Goods
from user.models import User


class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name='商品', on_delete=models.CASCADE)
    nums = models.IntegerField(default=0, verbose_name='数量')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    is_select = models.BooleanField(default=True)

    class Meta:
        db_table = 'f_shopping_cart'