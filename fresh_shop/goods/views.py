from random import randint

from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from goods.models import GoodsCategory, Goods
from utils.functions import is_login


def index(request):
    if request.method == 'GET':
        # 如果访问首页，返回渲染的首页index.html页面
        # 方式1：object ==> [GoodsCategory Object, [Goods objects1, objects2 ...]]
        # 方式2：object ==> {'c_name':[GoodsCategory Object, [Goods objects1, objects2 ...]]}
        categorys = GoodsCategory.objects.all()
        result = []
        for category in categorys:
            goods = category.goods_set.all()[:4]
            data = [category, goods]
            result.append(data)
        print(result)
        category_type = GoodsCategory.CATEGORY_TYPE
        return render(request, 'index.html', {'result': result, 'category_type': category_type})


def detail(request, id):
    if request.method == 'GET':
        rand = [randint(9, 44), randint(9, 44)]
        rand_goods = [Goods.objects.filter(pk=rand[0]).first(), Goods.objects.filter(id=rand[1]).first()]
        # 返回商品的详情信息
        goods = Goods.objects.filter(pk=id).first()
        return render(request, 'detail.html', {'goods': goods,'rand_goods':rand_goods})


def list(request):
    if request.method == 'GET':
        goods = Goods.objects.all()
        rand = [randint(9, 44), randint(9, 44)]
        rand_goods = [Goods.objects.filter(pk=rand[0]).first(), Goods.objects.filter(id=rand[1]).first()]
        # 分页
        page = int(request.GET.get('page', 1))

        pg = Paginator(goods, 10)
        goods = pg.page(page)

        return render(request, 'list.html', {'goods': goods, 'rand_goods': rand_goods})
