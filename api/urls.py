"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from one.views import *

urlpatterns = [
    path('admin/', admin.site.urls),  # 管理员
    path('categoryalldata/', categoryalldata),  # 商品所有分类数据
    path('wxusertest/', wxusertest),
    path('wxidgetproduct/', wxidgetproduct),  # 获取商品数据
    path('showcomment/', ShowCommentViews.as_view()),  # 获取商品对应的所有评论
    path('wxmycardata/', wxmycardata),  # 获取购物车数据
    path('wxgetalladdress/', wxgetalladdress),  # 获取地址数据
    path('wxaddaddress2/', wxaddaddress2),  # 新增地址
    path('wxdeladdress/', wxdeladdress),  # 删除地址
    path('wxChangeaddress/', wxChangeaddress),  # 修改地址
    path('wxaddressgotomypay/', wxaddressgotomypay),
    path('wxpayOrder/', wxpayOrder),  # 订单付款
    path('wxgotodindan/', wxgotodindan),  # 前往下单
    path('wxuseralldindan/', wxuseralldindan),  # 获取用户所有订单数据
    path('wxmyk/', wxmyk),  # 查询所有订单的物流实时情况
    path('wxwfh/', wxwfh),  # 待发货的订单
    path('wxwsh/', wxwsh),  # 待收货的订单
    path('wxwcm/', wxwcm),  # 待评论的订单
    path('wxadmintcm/', wxadmitcm),  # 用户发表评论
    path('wxadmitsh/', wxadmitsh),  # 用户确认收货

    path('wxcxadmin/', wxcxadmin),  # 后台登录
    path('mywxcx/', mywxcx, name='mywxcx'),  # 后台展示页
    path('wxfahuo/', wxfahuo, name='wxfahuo'),  # 发货处理函数
]
