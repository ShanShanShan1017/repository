from re import match

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import BjHouse
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db import connection
from django.db.models import Count, F, Q
from .models import BjHouse, UserViewHistory
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Value, CharField
from django.db.models.functions import Coalesce
# Create your views here.

# 欢迎页面
def index(request):
    return render(request, "index.html")

#登录页面
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('data')  # 假设data是你的数据页面的URL名称
        else:
            messages.error(request, '用户名或密码错误')
    return render(request, 'login.html')

# 主页面
def house_info_list(request):
    houses = BjHouse.objects.all()
    paginator = Paginator(houses, 10)  # 每页显示 10 条数据
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_admin = request.user.is_superuser  # 判断用户是否为管理员
    return render(request, 'data.html', {'page_obj': page_obj, 'is_admin': is_admin})

#注册界面
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, '用户名已存在')
            return redirect('register')  # 使用命名 URL

        # 密码强度校验（补充正则验证）
        if not match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
            messages.error(request, '密码需包含字母、数字和特殊字符，长度≥8位')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        messages.success(request, '注册成功，请登录')
        return redirect('login')  # 使用命名 URL

    return render(request, 'register.html')

#查找房源
def get_search_filters(request):
    # 获取所有唯一的城区（非空值，去重）
    chengqu_values = BjHouse.objects.filter(chengqu__isnull=False) \
        .exclude(chengqu='') \
        .values_list('chengqu', flat=True) \
        .distinct() \
        .order_by('chengqu')

    # 获取所有唯一的房型（非空值，去重）
    huxing_values = BjHouse.objects.filter(huxing__isnull=False) \
        .exclude(huxing='') \
        .values_list('huxing', flat=True) \
        .distinct() \
        .order_by('huxing')

    return JsonResponse({
        'chengqu': list(chengqu_values),
        'huxing': list(huxing_values),
    })


def search_houses(request):
    queryset = BjHouse.objects.all()

    # 城区筛选
    chengqu = request.GET.get('chengqu')
    if chengqu:
        queryset = queryset.filter(chengqu=chengqu)

    # 房型筛选
    huxing = request.GET.get('huxing')
    if huxing:
        queryset = queryset.filter(huxing=huxing)

    # 单价范围筛选（danjia_min 和 danjia_max）
    danjia_min = request.GET.get('danjia_min')
    danjia_max = request.GET.get('danjia_max')
    if danjia_min:
        queryset = queryset.filter(danjia__gte=float(danjia_min))
    if danjia_max:
        queryset = queryset.filter(danjia__lte=float(danjia_max))

    # 总价范围筛选（fangjia_min 和 fangjia_max）
    fangjia_min = request.GET.get('fangjia_min')
    fangjia_max = request.GET.get('fangjia_max')
    if fangjia_min:
        queryset = queryset.filter(fangjia__gte=float(fangjia_min))
    if fangjia_max:
        queryset = queryset.filter(fangjia__lte=float(fangjia_max))

    # 序列化结果
    houses = [{
        'id': house.id,
        'jianjie': house.jianjie,
        'xiaoqu': house.xiaoqu,
        'huxing': house.huxing,
        'mianji': house.mianji,
        'guanzhurenshu': house.guanzhurenshu,
        'guankancishu': house.guankancishu,
        'fabushijian': house.fabushijian,
        'fangjia': house.fangjia,
        'danjia': house.danjia,
        'chengqu': house.chengqu,
    } for house in queryset]

    return JsonResponse(houses, safe=False)

# 柱状图
def house_distribution(request):
    """获取各城区房源分布数据"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT chengqu, COUNT(*) as count FROM new01_bjhouse GROUP BY chengqu")
        results = cursor.fetchall()

    # 转换为JSON格式
    data = [{'chengqu': row[0], 'count': row[1]} for row in results]

    return JsonResponse(data, safe=False)

# 饼状图
def house_type_distribution(request):
    """获取各房型分布数据"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT huxing, COUNT(*) as count FROM new01_bjhouse GROUP BY huxing")
        results = cursor.fetchall()

    # 转换为JSON格式
    data = [{'fangxing': row[0], 'count': row[1]} for row in results]

    return JsonResponse(data, safe=False)


# 记录用户浏览历史
@login_required
def record_view_history(request,house_id):
    if request.method == 'POST':
        house = get_object_or_404(BjHouse, id=house_id)
        UserViewHistory.objects.create(user=request.user, house=house)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

# 基于用户浏览历史的推荐算法
@login_required
def recommend_houses(request):
    # 获取用户已浏览的房源
    viewed_houses = UserViewHistory.objects.filter(user=request.user).values_list('house_id', flat=True)
    all_houses = list(BjHouse.objects.exclude(id__in=viewed_houses))

    if not all_houses:
        return JsonResponse([], safe=False)

    if viewed_houses:
        # 创建用户浏览房源的特征矩阵
        viewed_house_objects = BjHouse.objects.filter(id__in=viewed_houses)
        feature_matrix = []
        for house in viewed_house_objects:
            features = [
                hash(house.xiaoqu) % 100,
                hash(house.chengqu) % 100,
                hash(house.huxing) % 100,
                house.mianji or 0,
                house.fangjia or 0,
                house.danjia or 0
            ]
            feature_matrix.append(features)

        # 计算平均特征向量作为推荐基础
        base_profile = np.mean(feature_matrix, axis=0)

        # 计算所有房源与基础向量的相似度
        similarity_scores = []
        for house in all_houses:
            house_features = [
                hash(house.xiaoqu) % 100,
                hash(house.chengqu) % 100,
                hash(house.huxing) % 100,
                house.mianji or 0,
                house.fangjia or 0,
                house.danjia or 0
            ]
            similarity = cosine_similarity([base_profile], [house_features])[0][0]
            similarity_scores.append((house, similarity))

        # 按相似度排序并取前10个
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        recommended_houses = [house for house, score in similarity_scores[:10]]
    else:
        # 如果用户没有浏览记录，随机选择10个房源作为推荐
        import random
        if len(all_houses) > 10:
            recommended_houses = random.sample(all_houses, 10)
        else:
            recommended_houses = all_houses

    # 准备推荐数据
    recommended_data = [
        {
            'id': house.id,
            'jianjie': house.jianjie,
            'xiaoqu': house.xiaoqu,
            'huxing': house.huxing,
            'mianji': house.mianji,
            'guanzhurenshu': house.guanzhurenshu,
            'guankancishu': house.guankancishu,
            'fabushijian': house.fabushijian,
            'fangjia': house.fangjia,
            'danjia': house.danjia,
            'chengqu': house.chengqu,
        }
        for house in recommended_houses
    ]

    return JsonResponse(recommended_data, safe=False)


@login_required
def house_detail(request, house_id):
    house = get_object_or_404(BjHouse, id=house_id)

    # 记录浏览历史（无论用户从何处访问房源详情）
    if request.user.is_authenticated:
        UserViewHistory.objects.get_or_create(user=request.user, house=house)

#管理员页面
@login_required
def administrator_view(request):
    if not request.user.is_superuser:
        return redirect('data')  # 如果不是管理员，重定向到普通数据页面
    houses = BjHouse.objects.all()
    paginator = Paginator(houses, 10)  # 每页显示 10 条数据
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_admin = request.user.is_superuser  # 判断用户是否为管理员
    return render(request, 'administrator.html', {'page_obj': page_obj, 'is_admin': is_admin})

#添加数据
@login_required
def add_house(request):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': '只有管理员可以添加房源'})
    if request.method == 'POST':
        try:
            jianjie = request.POST.get('jianjie')
            xiaoqu = request.POST.get('xiaoqu')
            huxing = request.POST.get('huxing')
            mianji = request.POST.get('mianji')
            guanzhurenshu = request.POST.get('guanzhurenshu')
            guankancishu = request.POST.get('guankancishu')
            fabushijian = request.POST.get('fabushijian')
            fangjia = request.POST.get('fangjia')
            danjia = request.POST.get('danjia')
            chengqu = request.POST.get('chengqu')
            jingdu = request.POST.get('jingdu')
            weidu = request.POST.get('weidu')

            BjHouse.objects.create(
                jianjie=jianjie,
                xiaoqu=xiaoqu,
                huxing=huxing,
                mianji=mianji,
                guanzhurenshu=guanzhurenshu,
                guankancishu=guankancishu,
                fabushijian=fabushijian,
                fangjia=fangjia,
                danjia=danjia,
                chengqu=chengqu,
                jingdu=jingdu,
                weidu=weidu
            )
            return JsonResponse({'success': True, 'message': '房源添加成功'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': '无效的请求方法'})

# @login_required
def delete_house(request, house_id):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': '只有管理员可以删除房源'})
    if request.method == 'POST':
        try:
            house = BjHouse.objects.get(id=house_id)
            house.delete()
            return JsonResponse({'success': True, 'message': '房源删除成功'})
        except BjHouse.DoesNotExist:
            return JsonResponse({'success': False, 'message': '房源不存在'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': '无效的请求方法'})
