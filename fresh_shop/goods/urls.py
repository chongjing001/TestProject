from django.urls import path

from goods import views

urlpatterns = [
    # 首页
    path('index/', views.index, name='index'),
    # 详情
    path('detail/<int:id>/', views.detail, name='detail'),

    # 搜索清单
    path('list/', views.list, name='list')

]
