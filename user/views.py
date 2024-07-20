from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import users
import json


@csrf_exempt
@require_http_methods(["GET", "POST"])
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        phone_number = data.get('phone_number')

        if users.objects.filter(username=username).exists():
            return JsonResponse({'message': '用户名已存在'}, status=400)

        if not username:
            return JsonResponse({'message': '用户名不能为空'}, status=400)

        # 创建用户
        user = users(username=username, email=email, phone_number=phone_number, password=password)
        user.save()

        return JsonResponse({'message': '注册成功'}, status=201)

    return JsonResponse({'message': 'Method Not Allowed'}, status=405)


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        received_name = data.get('username')
        received_password = data.get('password')
        user = users.objects.filter(username=received_name).first()

        if user:
            if received_password == received_password:
                if user.is_active:
                    login(request, user)  # 登录用户
                    print('success')
                    return JsonResponse({'message': '登录成功', 'code': 200})
                else:
                    return JsonResponse({'code': 200, 'msg': '用户未激活'})
            else:
                return JsonResponse(
                    {'msg': '用户名或密码错误',
                     'code': 400
                     })
        else:
            return JsonResponse({'msg': '用户不存在', 'code': 400})
    else:
        return JsonResponse({'msg': 'Method Not Allowed', 'code': 403})


def show_info(request):
    current_user = request.user
    print(current_user)
    try:
        # 假设 PersonalInfo 是你的数据库模型，包含 name、mail、tel 字段
        personal_info = users.objects.get(username=current_user.username)# 获取第一条个人信息记录

        if personal_info:
            data = {
                'username': personal_info.username,
                'email': personal_info.email,
                'phone_number': personal_info.phone_number
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'msg': 'Personal info not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
