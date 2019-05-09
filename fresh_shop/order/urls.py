from django.urls import path

from order import views

urlpatterns = [
    # 结算页面
    path('place_order/',views.place_order,name='place_order'),

    path('user_center/', views.user_center, name='user_center'),
    path('user_center_order/', views.user_center_order, name='user_center_order'),
    path('user_center_site/', views.user_center_site, name='user_center_site'),

    path('order/',views.order, name='order'),

]
