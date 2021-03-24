from django.contrib import admin
from .models import *  # 导入模型类

# Register your models here.

admin.site.site_header = "后台管理系统"
admin.site.site_title = "欢迎进入后台管理~"
admin.site.index_title = "XX项目"

# 在管理员页面注册，注册后才会显示出来
admin.site.register(WXCategory)
admin.site.register(WXGProduct)
admin.site.register(mywxuser)
admin.site.register(wxddaddress)
admin.site.register(wxdindan)
admin.site.register(wxcomment)

