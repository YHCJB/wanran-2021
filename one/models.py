from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class WXCategory(models.Model):
    title = models.CharField(null=True, blank=True, max_length=300)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
        verbose_name = '分类表'
        verbose_name_plural = '分类表'


class WXGProduct(models.Model):
    name = models.CharField('商品名', null=True, blank=False, max_length=300)
    cover_img = models.CharField('商品主图', null=True, blank=False, max_length=3000)
    attach_img_1 = models.CharField('商品幅图1', null=True, blank=True, max_length=3000)
    attach_img_2 = models.CharField('商品幅图2', null=True, blank=True, max_length=3000)
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    spec = models.TextField('描述', null=True, blank=True, default="None")
    total_sales = models.IntegerField('销售量', null=True, blank=True, default=0)
    category = models.ForeignKey(verbose_name='分类', to=WXCategory, on_delete=models.CASCADE)
    body = models.CharField('详情页', null=True, blank=True, max_length=3000)

    def __str__(self):
        return 'id %s,商品名：%s' % (self.id, self.name)

    class Meta:
        ordering = ['id']
        verbose_name = '商品表'
        verbose_name_plural = '商品表'


class mywxuser(models.Model):
    openid = models.CharField('微信openid', max_length=500, null=True, blank=True)
    nickname = models.CharField('微信签名', max_length=200, null=True, blank=True)
    gender = models.CharField('性别', max_length=2, null=True, blank=True)  # 1为男 0为女
    city = models.CharField('城市', max_length=200, null=True, blank=True)
    province = models.CharField('省', max_length=200, null=True, blank=True)
    country = models.CharField('国家', max_length=200, null=True, blank=True)
    avatar = models.CharField('微信头像URL', max_length=2000, null=True, blank=True)  # 头像
    phone = models.CharField('手机号', max_length=11, null=True, blank=True)
    c_time = models.DateTimeField('添加时间', auto_now=True, null=True, blank=True)
    token = models.CharField(max_length=3000, null=True, blank=True)
    expiration_time = models.DateTimeField(default=datetime.now, verbose_name="过期时间", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="token添加时间", null=True, blank=True)

    def __str__(self):
        return 'id %s,用户昵称：%s' % (self.id, self.nickname)

    class Meta:
        ordering = ['id']
        verbose_name = '用户表'
        verbose_name_plural = '用户表'


class wxddaddress(models.Model):
    auser = models.CharField('用户id', max_length=5)  # 关联User表多对一
    aname = models.CharField('收货人', max_length=60, null=True, blank=True)
    aphone = models.CharField('手机号', max_length=20, null=True, blank=True)
    city = models.CharField('省市', max_length=500, null=True, blank=True)
    aaddress = models.CharField('详细地址', max_length=500, null=True, blank=True)
    adefaultaddress = models.CharField('是否默认地址', max_length=5, default="2")  # (1, "默认地址"),(2, "普通地址")

    def __str__(self):
        return 'id %s,对应用户id：%s' % (self.id, self.auser)

    class Meta:
        ordering = ['id']
        verbose_name = '地址表'
        verbose_name_plural = '地址表'


class wxdindan(models.Model):
    wxuserid = models.CharField('用户id', max_length=1000, null=True, blank=True)  # 用户id
    wxopenid = models.CharField('用户openid', max_length=1000, null=True, blank=True)  # 用户openid
    wxusertext = models.CharField('用户备注', max_length=1000, null=True, blank=True)
    fapiao = models.CharField('发票抬头', max_length=1000, null=True, blank=True)
    fapiaohaoma = models.CharField('发票税号', max_length=1000, null=True, blank=True)
    paymode = models.CharField('支付方式', max_length=1000, null=True, blank=True, default=1)  # 默认为微信支付
    addressid = models.CharField('地址id', max_length=1000, null=True, blank=True)  # 地址id

    productid = models.CharField("商品id", max_length=1000, null=True, blank=True)
    count = models.CharField('购买数量', max_length=1000, null=True, blank=True)  # 单款商品的数量
    payzt = models.CharField('支付状态', max_length=1000, null=True, blank=True)  # 等待支付,或支付成功等等
    dindanbianhao = models.CharField('订单编号', max_length=200, null=True, blank=True)
    totalprice = models.CharField('总货款', max_length=200, null=True, blank=True)  # 单款商品的总价款
    add_time = models.DateTimeField(default=datetime.now, verbose_name="提交订单时间", null=True, blank=True)

    is_ship = models.CharField('是否已经发货', max_length=5, default="2")  # (1, "是"),(2, "否")
    is_receipt = models.CharField('是否确认收货', max_length=5, default="2")  # (1, "是"),(2, "否")
    is_comment = models.CharField('是否评价', max_length=5, default="2")  # (1, "是"),(2, "否")
    kuaidigonshi = models.CharField('快递公司', max_length=200, null=True, blank=True)
    kuaididanhao = models.CharField('快递单号', max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = '订单表'
        verbose_name_plural = '订单表'


# 关联:与用户表多对一,与地址表一对一,商品表没有设关联,
# 1为微信支付,   2为支付宝支付,,,还可以扩展更多方式
# 注,优化时,可以除掉有些重复的字段,比如wxopenid,放在这只是为了快速方便开发,不要让表关联太深,这样查询时,会拖慢后端,先设计如此,后期还会改
# 所有的关联已取消,为了写代码快,方便


class wxcomment(models.Model):
    wxuserid = models.CharField('用户id', max_length=1000, null=True, blank=True)
    wxgoodsid = models.CharField('商品id', max_length=1000, null=True, blank=True)
    content = models.CharField('评价内容', max_length=1000, null=True, blank=True)
    counts = models.IntegerField('评分', null=True, blank=True)
    comm_time = models.DateTimeField(default=datetime.now, verbose_name="提交评论时间", null=True, blank=True)

    def __str__(self):
        return '商品id %s,商品评分：%s' % (self.wxgoodsid, self.counts)

    class Meta:
        ordering = ['id']
        verbose_name = '评价表'
        verbose_name_plural = '评价表'


