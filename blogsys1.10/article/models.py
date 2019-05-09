from django.db import models


# Create your models here.
from user.models import User


class Article(models.Model):
    a_title = models.CharField(max_length=20, unique=True)
    a_part = models.CharField(max_length=20, default='你猜', null=True)
    a_tag = models.CharField(max_length=20, default='Django', null=True)
    a_date = models.DateField(auto_now_add=True)
    content = models.TextField(null=True)
    icon = models.ImageField(upload_to='upload', null=True)
    is_del = models.BooleanField(default=0)
    art = models.ForeignKey(User,on_delete=models.CASCADE,related_name='article',null=True)
    class Meta:
        db_table = 'article'




class Part(models.Model):
    p_name = models.CharField(max_length=20,unique=True)
    p_alias = models.CharField(max_length=20,default='还没想好',null=True)
    p_num = models.IntegerField(null=True)
    p = models.ManyToManyField(Article,related_name='part')

    class Meta:
        db_table = 'part'
