from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=150, null=False)
    crate_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=20)

    class Meta:
        db_table = 'user_token'
