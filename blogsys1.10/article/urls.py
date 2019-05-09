from django.urls import path

from article import views

urlpatterns = [
    # 后台首页
    path('index/', views.index, name='index'),
    # 栏目
    path('category/', views.category, name='category'),
    # 添加文章
    path('add_article/', views.add_article, name='add_article'),
    # 删除文章
    path('del_article/', views.del_article, name='del_article'),
    # 修改文章
    path('update_article/', views.update_article, name='update_article'),

    # 修改栏目
    path('update_category',views.update_category, name='update_category')
]
