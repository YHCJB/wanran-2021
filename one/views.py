from django.http import HttpResponse, JsonResponse
from rest_framework import serializers
from one.models import *
from urllib.parse import parse_qs, urlparse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from ShowapiRequest import ShowapiRequest
import json
import time
import datetime
import demjson  # 需要先安装 Demjson 模块之后才能使用


class sermywxGProduct(serializers.ModelSerializer):  # 序列化所有字段
    class Meta:
        model = WXGProduct  # #可以更换数据库
        fields = "__all__"  # 是否显示所有数据


def WXdddpro():
    shopcart_list = WXGProduct.objects.all()
    serializer = sermywxGProduct(shopcart_list, many=True)  # 序列化
    return serializer.data  # 把数据传出去


class sermywxGCategory(serializers.ModelSerializer):  # 并说明序列化所有字段
    class Meta:
        # model=ShopCart#获取所有购物车表中的数据，并序列化
        model = WXCategory  # 可以更换数据库,这是个接口
        fields = "__all__"  # 是否显示所有数据,也是个接口


def WXdddcate():
    shopcart_list = WXCategory.objects.all()
    serializer = sermywxGCategory(shopcart_list, many=True)  # 序列化
    return serializer.data  # 把数据传出去


def categoryalldata(request):
    mydata = {}
    mydata["data"] = []
    ccc = {}
    ppp = {}
    ccc = WXdddcate()  # 分类,字典
    ppp = WXdddpro()  # 商品,字典
    mydata["data"] = ccc
    for t, i in enumerate(mydata["data"]):
        print(i["id"])  # 拿到分类表所有id值,9个分类
        print("t", t)  # 输出的是循环下标0开始,0-8
        mydata["data"][t]["product"] = []  # 为每一个分类对象,添加一个product子对象
        for o in ppp:
            if o['category'] == i["id"]:
                mydata["data"][t]["product"].append(o)

    return JsonResponse(mydata, safe=False, json_dumps_params={'ensure_ascii': False})


def wxusertest(request):
    if request.method == "POST":  # 因为默认时get请求，所以要加条件
        # request.body里面是二进制数据，b'{"myuserinfo":{"nickname":...},"myopenid":"..."}'，<class 'bytes'>

        body_unicode = request.body.decode('utf-8')  # 通过 utf-8 把二进制数据转化为字符串
        print(body_unicode)  # 里面是字符串数据，{"myuserinfo":{"nickname":...},"myopenid":"..."}
        print(type(body_unicode))  # <class 'str'>

        body = demjson.encode(body_unicode)  # demjson.encode函数，可以将 Python 对象编码成 JSON 字符串
        # 里面是加了转义字符的字符串 "{\"myuserinfo\":{\"nickname\":...},\"myopenid\":\"...\"}"，<class 'str'>

        body = json.loads(body)
        # {"myuserinfo":{"nickname":...},"myopenid":"..."}，<class 'str'>

        params = parse_qs(body)
        # {}，<class 'dict'>

        data = json.loads(body)  # 将已编码的 JSON 字符串解码为 Python 对象
        # {'myuserinfo':{'nickname':...},'myopenid':'...'}，<class 'dict'>，json对象

        print("接收的openid", data["myopenid"])
        print("接收的用户信息", data['myuserinfo'])

        myopenid = data["myopenid"]
        userinfo = data['myuserinfo']

        # 处理性别,先不处理,让前端处理,因为从腾迅回调拿到的本来就是1 或 0

        # 在写入数据库前判断数据库中是否已有该openid的用户
        myppp = mywxuser.objects.filter(openid=myopenid)  # 如有,则不是空数组,如无,则为空数组
        # filter返回的是个数组，但是没有查询结果时并不会像get一样报错，即将get查询返回的对象放入一个数组

        if myppp:  # 如果不为空,已有该用户
            print(myppp[0].id)
            return HttpResponse(myppp[0].id)
        else:  # 如果不存在此用户
            mywxuser.objects.create(openid=myopenid, nickname=userinfo['nickName'], gender=userinfo['gender'], city=userinfo['city'], province=userinfo['province'], country=userinfo['country'], avatar=userinfo['avatarUrl'])

            # 来个保险,取出myuser表中,该用户的id,传到前端,User已存在,前端暂时用不着,先不管
            usertwo = mywxuser.objects.filter(openid=data["myopenid"])  # 结果为对象数组,里面只有一个对象
            getid = usertwo[0].id

            return HttpResponse(getid)
    else:
        return HttpResponse("这是一个GET请求")


class xiuwxidgetproduct(serializers.ModelSerializer):  # 并说明序列化所有字段
    class Meta:
        model = WXGProduct  # #可以更换数据库,这是个接口
        fields = "__all__"  # 是否显示所有数据,也是个接口


# 根据id查找商品
def wxidgetproduct(request):
    body_unicode = request.body.decode('utf-8')
    body = demjson.encode(body_unicode)
    body = json.loads(body)
    print(body)  # 前端获取并传递过来的id值，{"id":"4"}
    proid = json.loads(body)
    myid = proid['id']  # 取出了商品id值，4

    shopcart_list = WXGProduct.objects.filter(id=myid)  # 筛选id为4的商品
    serializer1 = xiuwxidgetproduct(shopcart_list, many=True)

    # 把数据库中的数据调出来，并序列化成json传到前端
    ttt = {}
    jjj = serializer1.data  # 取上面函数传出来的数据,是字典，OrderDict([('id',5),('name','..'),('cover_img','..')...])

    kkk = json.dumps(jjj)  # 把数据字典转为JSON对象格式,前端才可以用。[{"id":5,"name":"...","attach_img_1":... , "category":1}]

    ttt["kkk"] = kkk  # 赋值，回传
    return HttpResponse(kkk)  # 这个会直接覆盖网页中所有的数据


# 根据id查找评论
class ShowCommentViews(APIView):
    def post(self, request, *args, **kwargs):
        id = int(request.data['id'])
        commentList = []
        comment = wxcomment.objects.filter(wxgoodsid=id).values()
        for i in comment:
            commentList.append(i)
        print(commentList)
        return Response({"status": True, 'message': '试验成功', 'data': commentList})


# 获取购物车
def wxmycardata(request):
    body_unicode = request.body.decode('utf-8')  # 获取前端传回的数据 cardata
    body = demjson.encode(body_unicode)
    body = json.loads(body)  # 字符串 {"cardata":[{"id":"4","num":2},{"id":"6","num":1}

    proid = json.loads(body)  # <class 'dict'> , {'cartdata':[{'id':4,'num':2},{'id':6,'num':1}]}

    mmm = proid['cardata']  # 取出字典里的对象数组， [{'id': '4', 'num': 2}, {'id': '6', 'num': 1}]

    zzz = []

    for i in mmm:  # 循环取出商品的id，然后查找并返回商品名称
        pid = i['id']
        plist = WXGProduct.objects.get(id=pid)  # 用id查出商品,结果为商品对象数组
        zzz.append(plist)  # 加入数组，zzz的类型为 <class 'list'>

    serializer = xiuwxidgetproduct(zzz, many=True)  # 调用序列化器
    jjj = serializer.data
    # [OrderDict([('id',4),(..),.('category',1)])], <class 'rest_framework.utils.serializer_helpers.ReturnList'>

    kkk = json.dumps(jjj).encode('utf-8').decode('unicode_escape')  # 把数据字典转为JSON对象格式
    # [{"id":4,"name":"..",...}], <class 'str'>

    # 此时kkk为json对象, 在前端就是对象数组, mmm也是对象数组

    return HttpResponse(kkk)  # 这个会直接覆盖网页中所有的数据


class wxxiupro20(serializers.ModelSerializer):  # 并说明序列化所有字段
    class Meta:
        model = wxddaddress  # #可以更换数据库,这是个接口
        fields = "__all__"  # 是否显示所有数据,也是个接口


# 获取所有地址数据
def wxgetalladdress(request):
    print(request.body)
    body_unicode = request.body.decode('utf-8')
    body = demjson.encode(body_unicode)
    body = json.loads(body)
    print("我将参数转为字符串" + body)  # username=15323441764&addressid=15&productid=19&pnum=4&myprice=356
    print(type(body))  # <class 'str'>

    params = parse_qs(body)
    print(type(body))  # <class 'str'>
    data = json.loads(body)
    print("data", data)
    print("data类型", type(data))  # dict字典,json对象
    print("接收前端的id", data["myid"])
    myid = data["myid"]  # myid就是前端传过来的用户id了 ,

    shopcart_list = wxddaddress.objects.filter(auser=myid)  # 筛选再传到前端
    serializer = wxxiupro20(shopcart_list, many=True)
    # 把数据库数据调出来并序列化,成json传到前端

    jjj = serializer.data  # 取上面函数传出来的数据,是字典
    print(jjj)
    print("#" * 20)
    print(json.dumps(jjj))
    kkk = json.dumps(jjj)  # 把数据字典转为JSON对象格式,前端才可以用

    return HttpResponse(kkk)  # 这个会直接覆盖网页中所有的数据


# 新增地址
def wxaddaddress2(request):
    print(request.body)
    body_unicode = request.body.decode('utf-8')
    body = demjson.encode(body_unicode)
    body = json.loads(body)
    print("我将参数转为字符串" + body)  # username=15323441764&addressid=15&productid=19&pnum=4&myprice=356
    print(type(body))  # <class 'str'>

    params = parse_qs(body)
    print(type(body))  # <class 'str'>
    data = json.loads(body)
    print("data", data)
    print("data类型", type(data))  # dict字典,json对象
    print(data["addobj"])  # {'username': '2323', 'telphone': '212', 'address': '1231', 'default': 1, 'userid': 30}
    myobj = data["addobj"]  # {'username': '2323', 'telphone': '212', 'address': '1231', 'default': 1, 'userid': 30}

    userid = myobj['userid']
    myname = myobj['username']
    mcity = myobj['city']

    myphone = myobj['telphone']
    myaddress = myobj['address']
    myadefaultaddress = myobj['default']
    print(userid, myname, myphone, myaddress, myadefaultaddress)
    # 操作默认地址
    if myobj['default'] == 1:  # 写入的是默认地址,则要把之前的默认地址改为普通地址
        obja = wxddaddress.objects.filter(adefaultaddress=1)  # 测试数据库有无默认地址,数据库无数据,或无默认地址,返回为[]
        if obja:  # 如果有默认地址存在,先把默认地址设为普通地址
            print("8888888888888888888888888888")
            obja[0].adefaultaddress = 2
            obja[0].save()
            wxddaddress.objects.create(auser=userid, aname=myname, aphone=myphone, aaddress=myaddress,
                                       adefaultaddress=myadefaultaddress, city=mcity)
        else:  # 如果无默认地址存在,或数据库为空,则直接写入
            wxddaddress.objects.create(auser=userid, aname=myname, aphone=myphone, aaddress=myaddress,
                                       adefaultaddress=myadefaultaddress, city=mcity)
    else:  # 写入的是普通地址 ,直接写入
        wxddaddress.objects.create(auser=userid, aname=myname, aphone=myphone, aaddress=myaddress,
                                   adefaultaddress=myadefaultaddress, city=mcity)
    return HttpResponse("写入成功")


# 点击地址列表页list.vue的地址,就改为默认地址,
def wxaddressgotomypay(request):
    body_unicode = request.body.decode('utf-8')  # 获取前端传来的 item.id，即对应地址表的id
    body = demjson.encode(body_unicode)  # 解码
    body = json.loads(body)

    params = parse_qs(body)
    # print(type(body))  # <class 'str'>
    data = json.loads(body)

    myid = data["myid"]  # 保存好处理后的id

    # 仅接受唯一一个默认地址，因此需要进行判断
    ttt = wxddaddress.objects.filter(adefaultaddress=1)
    print(len(ttt))  # 为0表示还没有设置过默认地址，无需处理

    if len(ttt) > 0:  # 有默认地址时，将其修为普通地址
        obja = wxddaddress.objects.get(adefaultaddress=1)
        obja.adefaultaddress = 2
        obja.save()

    wxddaddress.objects.filter(id=myid).update(adefaultaddress=1)

    return HttpResponse("已设为默认地址")


# 删除地址
def wxdeladdress(request):
    print(request.body)
    body_unicode = request.body.decode('utf-8')
    body = demjson.encode(body_unicode)
    body = json.loads(body)
    print("我将参数转为字符串" + body)
    print(type(body))  # <class 'str'>

    params = parse_qs(body)
    print(type(body))  # <class 'str'>
    data = json.loads(body)
    print("data", data)
    print("data类型", type(data))  # dict字典,json对象
    print("接收前端的id", data["addressid"])
    myid = data["addressid"]
    wxddaddress.objects.filter(id=myid).delete()

    return HttpResponse("ok")


# 修改地址
def wxChangeaddress(request):
    print(request.body)
    body_unicode = request.body.decode('utf-8')
    body = demjson.encode(body_unicode)
    body = json.loads(body)
    print("我将参数转为字符串" + body)
    print(type(body))  # <class 'str'>

    params = parse_qs(body)
    print(type(body))  # <class 'str'>
    data = json.loads(body)
    print("data", data)
    print("data类型", type(data))  # dict字典,json对象
    print("接收前端的对象", data["addobj"])
    myobj = data["addobj"]

    aid = myobj['aid']
    myname = myobj['username']
    mcity = myobj['city']
    myphone = myobj['telphone']
    myaddress = myobj['address']
    myadefaultaddress = myobj['default']
    print(aid, myname, myphone, myaddress, myadefaultaddress, mcity)
    # 操作默认地址
    if myobj['default'] == 1:  # 如果添加的地址设了默认地址,则要把之前的默认地址改为普通地址
        # 先测试默认地址
        ttt = wxddaddress.objects.filter(adefaultaddress=1)
        print(len(ttt))  # 0无默认地址时
        if len(ttt) > 0:  # 有默认地址才操作
            obja = wxddaddress.objects.get(adefaultaddress=1)
            print("obja", obja)  # 为[],如无默认地址
            obja.adefaultaddress = 2
            obja.save()

    wxddaddress.objects.filter(id=aid).update(aname=myname, aphone=myphone, city=mcity,
                                              aaddress=myaddress, adefaultaddress=myadefaultaddress)

    return HttpResponse("已成功修改")


# 生成商品订单号,时间精确到微秒
def getWxPayOrdrID():
    date = datetime.datetime.now()
    payOrderID = date.strftime("%Y%m%d%H%M%S%f")

    return payOrderID


# 支付的主函数，返回给前端的
def wxpayOrder(request):
    body_unicode = request.body.decode('utf-8')
    body = demjson.encode(body_unicode)
    body = json.loads(body)  # <class 'str'>

    params = parse_qs(body)
    data = json.loads(body)
    print("data", data)  # dict字典,json对象
    print("接收前端的对象", data['wxcartobj'])  # 取到对象
    a = data['wxcartobj']

    myopenid = a['kkkopenid']  # 取到用户openid
    myuserinfo = a['kkkuser']  # 取到微信用户签名头像等详息
    mycartarray = a['kkkobj']  # 取到购物车对象数组
    myuserid = a['wxuserid']  # 取到操作的用户的id

    # 计算要付的总金额
    totalprice = 0
    for i in range(0, len(mycartarray)):
        price = float(mycartarray[i]["price"]) * float(mycartarray[i]["num"])
        totalprice = totalprice + price
    print(totalprice)

    # 获取价格,和用户
    price = totalprice
    user_id = myuserid
    openid = myopenid

    order_num = getWxPayOrdrID()  # 生成订单号
    timeStamp = str(int(time.time()))  # 生成时间戳
    payzt = "SUCCESS"  # 支付状态，默认为成功支付，主要为了测试

    print("订单号", order_num)

    # 封装返回给前端的数据
    data = {"order_num": order_num, "price": price, "payzt": payzt, "timeStamp": timeStamp}
    kkk = json.dumps(data).encode('utf-8').decode('unicode_escape')  # 把数据字典转为JSON对象格式(str类型)
    return HttpResponse(kkk)


# 支付成功后数据入库（因为订单有一个24小时的有效时间，所以另外设置一个函数来处理数据入库）
def wxgotodindan(request):
    body_unicode = request.body.decode('utf-8')
    body = demjson.encode(body_unicode)
    body = json.loads(body)
    params = parse_qs(body)
    data = json.loads(body)

    print("接收前端的对象", data['wxcartobj'])  # 取到对象
    a = data['wxcartobj']  # a 里面包括要写入数据库的所有数据

    myopenid = a['kkkopenid']  # 取到用户openid
    myuserinfo = a['kkkuser']  # 取到微信用户签名头像等详息
    mycartarray = a['kkkobj']  # 取到购物车对象数组
    myuserid = a['wxuserid']  # 取到操作的用户的id
    order_num = a['order_num']  # 取到订单编号

    print("myopenid", myopenid)
    print("myuserinfo", myuserinfo)
    print("mycartarray", mycartarray)
    print("myuserid", myuserid)
    print("order_num", order_num)

    # 取地址表默认地址(不用前端传，因为不管怎样下单的都是默认地址)
    e = wxddaddress.objects.get(adefaultaddress=1)
    myaddressid = e.id  # 获得地址ID
    print("取得默认地址的id", myaddressid)

    data = {}
    paidthing = []

    # 写入数据库,一款商品就写入一条订单
    for i in range(0, len(mycartarray)):
        mytotalprice = float(mycartarray[i]["price"]) * float(mycartarray[i]["num"])
        myproid = mycartarray[i]['id']
        mycount = mycartarray[i]['num']

        wxdindan.objects.create(wxuserid=myuserid, wxopenid=myopenid, wxusertext="", fapiao="", fapiaohaoma="",
                                paymode="1", addressid=myaddressid, productid=myproid, count=mycount,
                                payzt="SUCCESS", dindanbianhao=order_num, totalprice=mytotalprice)

        paidthing.append(mycartarray[i]['id'])

    data['paidGoods'] = paidthing

    return JsonResponse(data)


class wxxiupro30(serializers.ModelSerializer):  # 序列化器订单表
    class Meta:
        model = wxdindan
        fields = "__all__"
        depth = 1


class wxxiupro31(serializers.ModelSerializer):  # 序列化器商品表
    class Meta:
        model = WXGProduct
        fields = "__all__"
        depth = 1


class wxxiupro32(serializers.ModelSerializer):  # 序列化器地址表
    class Meta:
        model = wxddaddress
        fields = "__all__"
        depth = 1


# 查看所有订单（整合多表数据与字典，到前端进行进一步整合）
def wxuseralldindan(request):
    body_unicode = request.body.decode('utf-8')  # 前端传来的是发出请求的用户的id
    body = demjson.encode(body_unicode)
    body = json.loads(body)

    params = parse_qs(body)
    data = json.loads(body)
    print("接收前端的对象", data['uid'])  # 经过数据处理后，取出id
    a = data['uid']

    # 去订单表，取所有订单的QuerySet对象
    e = wxdindan.objects.filter(wxuserid=a)
    print(e)  # 取到该用户的所有订单,是一个对象数组（查具体值用value）

    # 去商品表，取出涉及到的商品的QuerySet对象
    oproduct = []
    for item in e:  # 循环订单表获取到的QuerySet对象
        k = WXGProduct.objects.get(id=item.productid)  # 取出每一条具体的对应的商品id
        if k not in oproduct:  # k值去重操作
            oproduct.append(k)
    print("取出来的商品表对象数组", oproduct)

    # 去地址表，取出涉及到的地址的QuerySet对象
    oaddress = []
    for item in e:  # 循环每一条订单
        k = wxddaddress.objects.get(id=item.addressid)
        if k not in oaddress:  # 去重
            oaddress.append(k)
    print("取出来的商品表对象数组", oaddress)

    # 把数据库数据调出来，并序列化成json，传回到前端
    serializer = wxxiupro30(e, many=True)
    ttt = {}  # 定义空字典
    # 分别调用前面定义好的序列化器来对数据进行序列化
    jjj = serializer.data  # 取上面函数传出来的数据,是字典
    kdindan = json.dumps(jjj).encode('utf-8').decode('unicode_escape')  # 把数据字典转为JSON对象格式,前端才可以用

    serializer2 = wxxiupro31(oproduct, many=True)
    jjj2 = serializer2.data
    kproduct = json.dumps(jjj2).encode('utf-8').decode('unicode_escape')

    serializer3 = wxxiupro32(oaddress, many=True)
    jjj3 = serializer3.data
    kaddress = json.dumps(jjj3).encode('utf-8').decode('unicode_escape')

    # 把所有数据整合到kkk字典里，传回
    ttt["kdindan"] = kdindan
    ttt['kproduct'] = kproduct
    ttt['kaddress'] = kaddress

    return JsonResponse(ttt)


# 调用接口获取快递数据（物流跟踪函数）
def get_wuliu(num):
    r = ShowapiRequest("http://route.showapi.com/2435-1", "558570", "7ce8ce42cb5e4635ad7700d7dc97b706")
    r.addBodyPara("nuo", num)
    res = r.post()
    return res.text


# 处理订单表里的日期字段无法被json化的问题
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


# 返回所有未发货的订单（is_ship = 2）
def wxwfh(request):
    mydata = wxdindan.objects.filter(is_ship=2)

    # 去商品表，取出涉及到的商品的QuerySet对象
    oproduct = []
    for item in mydata:  # 循环订单表获取到的QuerySet对象
        k = WXGProduct.objects.get(id=item.productid)  # 取出每一条具体的对应的商品id
        if k not in oproduct:  # k值去重操作
            oproduct.append(k)

    # 去地址表，取出涉及到的地址的QuerySet对象
    oaddress = []
    for item in mydata:  # 循环每一条订单
        k = wxddaddress.objects.get(id=item.addressid)
        if k not in oaddress:  # 去重
            oaddress.append(k)

    # 把数据库数据调出来，并序列化成json，传回到前端
    serializer = wxxiupro30(mydata, many=True)
    ttt = {}  # 定义空字典
    # 分别调用前面定义好的序列化器来对数据进行序列化
    jjj = serializer.data  # 取上面函数传出来的数据,是字典
    kdindan = json.dumps(jjj, cls=DateEncoder).encode('utf-8').decode('unicode_escape')  # 把数据字典转为JSON对象格式,前端才可以用

    serializer2 = wxxiupro31(oproduct, many=True)
    jjj2 = serializer2.data
    kproduct = json.dumps(jjj2).encode('utf-8').decode('unicode_escape')

    serializer3 = wxxiupro32(oaddress, many=True)
    jjj3 = serializer3.data
    kaddress = json.dumps(jjj3).encode('utf-8').decode('unicode_escape')

    # 把所有数据整合到ttt字典里，传回
    ttt["kdindan"] = kdindan
    ttt['kproduct'] = kproduct
    ttt['kaddress'] = kaddress

    return JsonResponse(ttt)


# 返回所有待收货的订单（is_receipt = 2 )
def wxwsh(request):
    mydata = wxdindan.objects.filter(Q(is_receipt=2), Q(is_ship=1))

    # 去商品表，取出涉及到的商品的QuerySet对象
    oproduct = []
    for item in mydata:  # 循环订单表获取到的QuerySet对象
        k = WXGProduct.objects.get(id=item.productid)  # 取出每一条具体的对应的商品id
        if k not in oproduct:  # k值去重操作
            oproduct.append(k)

    # 去地址表，取出涉及到的地址的QuerySet对象
    oaddress = []
    for item in mydata:  # 循环每一条订单
        k = wxddaddress.objects.get(id=item.addressid)
        if k not in oaddress:  # 去重
            oaddress.append(k)

    # 把数据库数据调出来，并序列化成json，传回到前端
    serializer = wxxiupro30(mydata, many=True)

    ttt = {}  # 定义空字典
    # 分别调用前面定义好的序列化器来对数据进行序列化
    jjj = serializer.data  # 取上面函数传出来的数据,是字典
    kdindan = json.dumps(jjj, cls=DateEncoder).encode('utf-8').decode('unicode_escape')  # 把数据字典转为JSON对象格式,前端才可以用

    serializer2 = wxxiupro31(oproduct, many=True)
    jjj2 = serializer2.data
    kproduct = json.dumps(jjj2).encode('utf-8').decode('unicode_escape')

    serializer3 = wxxiupro32(oaddress, many=True)
    jjj3 = serializer3.data
    kaddress = json.dumps(jjj3).encode('utf-8').decode('unicode_escape')

    # 把所有数据整合到ttt字典里，传回
    ttt["kdindan"] = kdindan
    ttt['kproduct'] = kproduct
    ttt['kaddress'] = kaddress

    return JsonResponse(ttt)


# 返回所有待评论的订单（is_comment = 2）
def wxwcm(request):
    mydata = wxdindan.objects.filter(Q(is_comment=2), Q(is_receipt=1))

    # 去商品表，取出涉及到的商品的QuerySet对象
    oproduct = []
    for item in mydata:  # 循环订单表获取到的QuerySet对象
        k = WXGProduct.objects.get(id=item.productid)  # 取出每一条具体的对应的商品id
        if k not in oproduct:  # k值去重操作
            oproduct.append(k)

    # 去地址表，取出涉及到的地址的QuerySet对象
    oaddress = []
    for item in mydata:  # 循环每一条订单
        k = wxddaddress.objects.get(id=item.addressid)
        if k not in oaddress:  # 去重
            oaddress.append(k)

    # 把数据库数据调出来，并序列化成json，传回到前端
    serializer = wxxiupro30(mydata, many=True)

    ttt = {}  # 定义空字典
    # 分别调用前面定义好的序列化器来对数据进行序列化
    jjj = serializer.data  # 取上面函数传出来的数据,是字典
    kdindan = json.dumps(jjj, cls=DateEncoder).encode('utf-8').decode('unicode_escape')  # 把数据字典转为JSON对象格式,前端才可以用

    serializer2 = wxxiupro31(oproduct, many=True)
    jjj2 = serializer2.data
    kproduct = json.dumps(jjj2).encode('utf-8').decode('unicode_escape')

    serializer3 = wxxiupro32(oaddress, many=True)
    jjj3 = serializer3.data
    kaddress = json.dumps(jjj3).encode('utf-8').decode('unicode_escape')

    # 把所有数据整合到ttt字典里，传回
    ttt["kdindan"] = kdindan
    ttt['kproduct'] = kproduct
    ttt['kaddress'] = kaddress

    return JsonResponse(ttt)


# 返回所有订单的物流跟踪数据
def wxmyk(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = demjson.encode(body_unicode)
        body = json.loads(body)

        params = parse_qs(body)
        data = json.loads(body)

        yundan = data["mynum"]
        finaldata = get_wuliu(yundan)

        str_json = json.dumps(json.loads(finaldata)['showapi_res_body']['context'])

        return HttpResponse(str_json)
    else:
        return HttpResponse("这是一个GET请求")


# 确认收货
def wxadmitsh(request):
    body_unicode = request.body.decode('utf-8')
    body = demjson.encode(body_unicode)
    body = json.loads(body)

    params = parse_qs(body)
    data = json.loads(body)

    theid = data["theid"]
    wxdindan.objects.filter(id=theid).update(is_receipt=1)

    return HttpResponse("收货成功")


# 发表评论
def wxadmitcm(request):
    # 先判断有没有确认收货
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = demjson.encode(body_unicode)
        body = json.loads(body)

        params = parse_qs(body)
        data = json.loads(body)

        theuid = data["uid"]  # 用户id
        thegid = data["gid"]  # 商品id
        thecid = data["mm"]  # 当前订单id
        thecon = data["content"]  # 评论内容
        thecnt = data["count"]  # 评分

        print(theuid)
        print(thegid)
        print(thecon)
        print(thecnt)

        wxcomment.objects.create(wxuserid=theuid, wxgoodsid=thegid, content=thecon, counts=thecnt)
        wxdindan.objects.filter(id=thecid).update(is_comment=1)
        return HttpResponse("评论成功")


# 返回发货管理后台的视图
def wxcxadmin(request):
    return render(request, 'wxcxadmin.html')


# 后台登录页
def mywxcx(request):
    return render(request, 'mywxcx.html')


# 正式后台页面，需要进行登录验证
def mywxcx(request):
    # 验证密码并保存session
    if request.method == "POST":
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        print('用户名和密码是:', username, password)
        user = authenticate(username=username, password=password)
        print('user的值为:---', user)  # 登陆的用户名
        if user is not None:
            if user.is_active:
                login(request, user)
                print('登陆成功,进入后台了')
                filterdata = wxdindan.objects.filter(Q(payzt="SUCCESS"), Q(kuaididanhao=None) | Q(kuaididanhao=''))
                print(filterdata)

                # 结合商品表和地址表
                if filterdata.count() > 0:  # 如果有新订单,就结合,无的话,什么也不做(表示没有人付款买东西)
                    print("有新订单要发货")
                    # 开始结合
                    for index, val in enumerate(filterdata):
                        print(index, val)
                        print(val.payzt)
                        did = val.addressid  # 取地址id
                        print("地址id---", did)
                        xid = val.productid  # 取商品id
                        print("商品id---", xid)

                        # 取地址,进行结合
                        myaddress = wxddaddress.objects.filter(id=did)[0]
                        val.address = myaddress
                        print('加进去的地址', val.address)
                        print('加进去的地址城市', val.address.city)

                        # 取商品,进行结合
                        myproduct = WXGProduct.objects.filter(id=xid)[0]
                        val.product = myproduct
                        print('加进去的商品', val.product)
                        print('加进去的商品名称', val.product.name)

                return render(request, 'mywxcx.html', locals())

            else:
                print('登陆失败,返回登陆页接着登陆')
                return render(request, 'wxcxadmin.html')
        else:  # 如果用户名或密码不对
            return render(request, 'wxcxadmin.html')
    else:
        # 非POST请求,展示登陆页
        return render(request, 'wxcxadmin.html')


def wxfahuo(request):
    if request.method == "POST":
        mycom = request.POST.get('mycomcom').strip()
        mynum = request.POST.get('mynumnum').strip()
        mydindanid = request.POST.get('dindanid').strip()
        print('快递公司和快递单号和订单id是:', mycom, mynum, mydindanid)

        # 发货之后修改好运单数据和发货状态
        wxdindan.objects.filter(id=mydindanid).update(kuaidigonshi=mycom, kuaididanhao=mynum, is_ship=1)

        # 跳转回原页面，需要再渲染一次
        # 重新获得一次付款后,没有发货的订单
        filterdata = wxdindan.objects.filter(Q(payzt="SUCCESS"), Q(kuaididanhao=None) | Q(kuaididanhao=''))
        print('888', filterdata)
        # 结合商品表和地址表
        if filterdata.count() > 0:  # 如果有新订单,就结合,无的话,什么也不做(表示没有人付款买东西)
            print("有新订单要发货")
            # 开始结合
            for index, val in enumerate(filterdata):
                print(index, val)
                print(val.payzt)  # SUCCESS
                did = val.addressid  # 取地址id
                print("地址id---", did)
                xid = val.productid  # 取商品id
                print("商品id---", xid)

                # 取地址,进行结合
                myaddress = wxddaddress.objects.filter(id=did)[0]
                val.address = myaddress
                print('加进去的地址', val.address)
                print('加进去的地址城市', val.address.city)

                # 取商品,进行结合
                myproduct = WXGProduct.objects.filter(id=xid)[0]
                val.product = myproduct
                print('加进去的商品', val.product)
                print('加进去的商品名称', val.product.name)

        return render(request, 'mywxcx.html', locals())



