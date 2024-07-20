import json

import scipy.stats
from django.db.models import Max
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404
import pandas as pd
import pymysql
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scipy.interpolate import interp1d
import numpy as np
from formulation.models import formulations
from fileupload.models import FileContent
from rhdata.models import rheological_data
from temperature.models import temperature
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit


# index
def index(request):
    if request.method == 'GET':
        return render(request, "add_formulation.html")


# Excel文件处理与数据添加
def formulation_upload(request):
    if request.method == 'GET':
        return render(request, "add_formulation.html")
    # 读取Excel文件
    elif request.method == 'POST' and request.FILES['file']:
        title = request.POST['title']
        formulations_file = request.FILES['file']
        print("上传文件名:", formulations_file.name)
        FileContent.objects.create(title=title, files=formulations_file)
        df = pd.read_excel(formulations_file, engine='openpyxl')
        column_mapping = {
            '序号': 'formulation_id',
            'name': 'formulation_name',
            'PBT': 'pbt',
            'TDI': 'tdi',
            '三苯基铋': 'tri_bis',
            'A3': 'athree',
            'T313': 'bonding_agent',
            'AP（40-60目）': 'ap_small',
            'AP（100-140目）': 'ap_large',
            'Al粉': 'ai_powder',
            '交联剂TMP（三羟甲基丙烷）': 'tmp',
            '扩链剂（二乙二醇）': 'die_gly',
            '扩链剂（三乙二醇）': 'tri_glycol',
            '在R值的前提下，再需要添加的TDI的量': 'add_tdi'
        }
        # 替换列名
        df = df.rename(columns=column_mapping)
        # 将NaN值替换为0
        df = df.fillna(0)
        df = df.replace({'[g]': ''}, regex=True)
        # 将数据转换为字典形式的列表
        data_list = df.to_dict('records')
        print(data_list)
        pymysql.install_as_MySQLdb()
        # 将数据添加到数据库
        for data in data_list:
            formulations.objects.create(**data)
        # 保存更改到数据库
        connection.close()
        return render(request, "success.html", {"msg": "上传成功"})
    else:
        return HttpResponse('文件上传失败')


def formulation_list(request):
    if request.method == 'GET':
        formulation_id = request.GET.get('id')  # 获取前端传递的配方ID参数
        if formulation_id:
            try:
                formulation_id = int(formulation_id)
                formulation = formulations.objects.get(formulation_id=formulation_id)  # 根据配方ID查询配方信息
                # 这里可以根据实际情况组装需要返回的数据，比如将配方信息转换为字典格式
                formulation_data = {
                    'formulation_id': formulation.formulation_id,
                    'formulation_name': formulation.formulation_name,
                    'pbt': formulation.pbt,
                    'tdi': formulation.tdi,
                    'tri_bis': formulation.tri_bis,
                    'athree': formulation.athree,
                    'bonding_agent': formulation.bonding_agent,
                    'ap_small': formulation.ap_small,
                    'ap_large': formulation.ap_large,
                    'ai_powder': formulation.ai_powder,
                    'tmp': formulation.tmp,
                    'die_gly': formulation.die_gly,
                    'tri_glycol': formulation.die_gly,
                    'add_tdi': formulation.add_tdi
                }
                return JsonResponse({'formulations': [formulation_data]})  # 返回查询到的配方信息
            except formulations.DoesNotExist:
                return JsonResponse({'error': '配方不存在'}, status=404)  # 配方不存在的错误提示
        else:
            all_formulations = formulations.objects.all()  # 获取所有配方信息
            # 组装所有配方信息，这里示意为将配方信息列表转换为字典格式
            all_formulations_data = [{'formulation_id': f.formulation_id,
                                      'formulation_name': f.formulation_name,
                                      'pbt': f.pbt,
                                      'tdi': f.tdi,
                                      'tri_bis': f.tri_bis,
                                      'athree': f.athree,
                                      'bonding_agent': f.bonding_agent,
                                      'ap_small': f.ap_small,
                                      'ap_large': f.ap_large,
                                      'ai_powder': f.ai_powder,
                                      'tmp': f.tmp,
                                      'die_gly': f.die_gly,
                                      'tri_glycol': f.die_gly,
                                      'add_tdi': f.add_tdi} for f in all_formulations]
            return JsonResponse({'formulations': all_formulations_data})  # 返回所有配方信息

    return JsonResponse({'error': '请求方法不支持'}, status=405)


# 添加配方
@csrf_exempt
def formulation_add(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        # 将空字符串值替换为 0
        for key, value in data.items():
            if value == "":
                data[key] = "0"
        formulation = formulations(
            formulation_id=data['formulation_id'],
            formulation_name=data['formulation_name'],
            pbt=float(data['pbt']),
            tdi=float(data['tdi']),
            tri_bis=float(data['tri_bis']),
            athree=float(data['athree']),
            bonding_agent=float(data['bonding_agent']),
            ap_small=float(data['ap_small']),
            ap_large=float(data['ap_large']),
            ai_powder=float(data['ai_powder']),
            tmp=float(data['tmp']),
            die_gly=float(data['die_gly']),
            tri_glycol=float(data['tri_glycol']),
            add_tdi=float(data['add_tdi']),
        )
        formulation.save()

        return JsonResponse({'message': '配方添加成功'})
    else:
        return JsonResponse({'message': '无效的请求方法'}, status=405)


# 编辑配方
@csrf_exempt
def formulation_update(request, formulation_id):
    try:
        formulation = formulations.objects.get(formulation_id=formulation_id)
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            formulation.formulation_name = data['formulation_name']
            formulation.pbt = float(data['pbt'])
            formulation.tdi = float(data['tdi'])
            formulation.tri_bis = float(data['tri_bis'])
            formulation.athree = float(data['athree'])
            formulation.bonding_agent = float(data['bonding_agent'])
            formulation.ap_small = float(data['ap_small'])
            formulation.ap_large = float(data['ap_large'])
            formulation.ai_powder = float(data['ai_powder'])
            formulation.tmp = float(data['tmp'])
            formulation.die_gly = float(data['die_gly'])
            formulation.tri_glycol = float(data['tri_glycol'])
            formulation.add_tdi = float(data['add_tdi'])

            formulation.save()

            return JsonResponse({'message': '配方编辑成功'})
        else:
            return JsonResponse({'message': '无效的请求方法'}, status=405)
    except formulations.DoesNotExist:
        return JsonResponse({'message': '配方不存在'}, status=404)


@csrf_exempt
def formulation_del(request, formulation_id):
    try:
        formulation = formulations.objects.get(formulation_id=formulation_id)
        formulation.delete()
        return JsonResponse({'message': '配方删除成功'})
    except formulations.DoesNotExist:
        return JsonResponse({'message': '配方不存在'}, status=404)


# 时间-模量图
def time_mod_fig(request, formulation_id):
    def calculate_derivative(data_list, index, solidification_value1, solidification_value2):
        if index == 0 or index == len(data_list) - 1:
            return None  # Derivative cannot be calculated at the endpoints
        else:
            time_diff = data_list[index]['time_s'] - data_list[index - 1]['time_s']
            solidification_diff = solidification_value1 - solidification_value2
            derivative = solidification_diff / time_diff
            return derivative

    # 根据formulation_id获取相应的formulations对象
    formulation = get_object_or_404(formulations, formulation_id=formulation_id)

    # 获取与该formulation_id相关的rheological_data对象
    related_data = rheological_data.objects.filter(formulation_id=formulation_id).values('rh_id', 'temperature_id_id',
                                                                                         'time_s',
                                                                                         'time_min', 'loss_mod',
                                                                                         'energy_storage_mod',
                                                                                         'loss_factor',
                                                                                         'complex_viscosity')
    # 对related_data进行均匀抽样，每隔200条数据抽样一次
    sampled_data = []
    for i, data in enumerate(related_data):
        if i % 200 == 0:
            sampled_data.append(data)
    # 寻找energy_storage_mod与loss_mod相等时的数据，并取出特定条件下的数据
    gelPoint_data = []
    curPoint_data = []
    solidification_list_55 = []
    solidification_list_60 = []
    solidification_list_65 = []
    for temp_id in set(data['temperature_id_id'] for data in related_data):
        temp_related_data = [data for data in related_data if data['temperature_id_id'] == temp_id]
        max_mod = rheological_data.objects.filter(
            formulation_id=formulation.formulation_id,
            temperature_id=temp_id
        ).aggregate(max_energy_storage_mod=Max('energy_storage_mod'))['max_energy_storage_mod']
        min_mod = rheological_data.objects.filter(formulation_id=formulation_id,
                                                  temperature_id=temp_id).values(
            'energy_storage_mod').first()['energy_storage_mod']
        for i, data in enumerate(temp_related_data):
            # 固化度计算
            solidification_value = (data['energy_storage_mod'] - min_mod) / (max_mod - min_mod)
            time_s_value = data['time_s']
            if temp_id == 1:
                solidification_list_55.append({
                    'solidification': solidification_value,
                    'time_s': time_s_value
                })
            elif temp_id == 2:
                solidification_list_60.append({
                    'solidification': solidification_value,
                    'time_s': time_s_value
                })
            elif temp_id == 3:
                solidification_list_65.append({
                    'solidification': solidification_value,
                    'time_s': time_s_value
                })
    for temp_id in set(data['temperature_id_id'] for data in related_data):
        temp_related_data = [data for data in related_data if data['temperature_id_id'] == temp_id]
        current_data_index = 0  # 当前数据点的索引，为寻找固化点做准备，固化点一定在凝胶点之后，故而省去凝胶点之前的数据遍历
        solidification_list = []
        other_list1 = []
        other_list2 = []
        if temp_id == 1:
            solidification_list = solidification_list_55
            other_list1 = solidification_list_60
            other_list2 = solidification_list_65
        elif temp_id == 2:
            solidification_list = solidification_list_60
            other_list1 = solidification_list_55
            other_list2 = solidification_list_65
        elif temp_id == 3:
            solidification_list = solidification_list_65
            other_list1 = solidification_list_60
            other_list2 = solidification_list_55
        for i, data in enumerate(temp_related_data):
            if abs(data['energy_storage_mod'] - data['loss_mod']) < 0.03 * data['energy_storage_mod']:
                solidification_value = solidification_list[i]['solidification']
                solidification_value1 = solidification_list[i - 1]['solidification']
                # 计算固化速率
                derivative_value = calculate_derivative(temp_related_data, i, solidification_value,
                                                        solidification_value1)
                derivative_other1 = 0
                derivative_other2 = 0
                now_i = i
                j = 0
                k = 0
                # 计算表观活化能
                for j in range(len(other_list1)):
                    if abs(solidification_value - other_list1[j]['solidification'] <= 0.08 * solidification_value):
                        solid_diff = other_list1[j]['solidification'] - other_list1[j - 1]['solidification']
                        time_diff = other_list1[j]['time_s'] - other_list1[j - 1]['time_s']
                        derivative_other1 = solid_diff / time_diff
                        break
                for k in range(len(other_list2)):
                    if abs(solidification_value - other_list2[k]['solidification'] <= 0.08 * solidification_value):
                        solid_diff = other_list2[k]['solidification'] - other_list2[k - 1]['solidification']
                        time_diff = other_list2[k]['time_s'] - other_list2[k - 1]['time_s']
                        derivative_other2 = solid_diff / time_diff
                        break
                x = [(55 + 273.15) ** -1, (60 + 273.15) ** -1, (65 + 273.15) ** -1]
                energy = 0
                if energy <= 0:
                    j += 1
                    k += 1
                    now_i += 1
                    while j <= len(other_list1) and k <= len(other_list2) and now_i <= len(temp_related_data):
                        solidification_value = solidification_list[now_i]['solidification']
                        solidification_value1 = solidification_list[now_i - 1]['solidification']
                        derivative_value = calculate_derivative(temp_related_data, now_i, solidification_value,
                                                                solidification_value1)
                        solid_diff = other_list1[j]['solidification'] - other_list1[j - 1]['solidification']
                        time_diff = other_list1[j]['time_s'] - other_list1[j - 1]['time_s']
                        derivative_other1 = solid_diff / time_diff
                        solid_diff = other_list2[k]['solidification'] - other_list2[k - 1]['solidification']
                        time_diff = other_list2[k]['time_s'] - other_list2[k - 1]['time_s']
                        derivative_other2 = solid_diff / time_diff
                        if derivative_value > 0 and derivative_other1 > 0 and derivative_other2 > 0:
                            y = [np.log(derivative_value), np.log(derivative_other1), np.log(derivative_other2)]
                            slope, intercept, _, _, _ = scipy.stats.linregress(x, y)
                            energy = -slope * 8.314
                            if energy <= 0:
                                j += 1
                                k += 1
                                now_i += 1
                            else:
                                break
                        elif derivative_value <= 0:
                            now_i += 1
                        elif derivative_other1 <= 0:
                            j += 1
                        elif derivative_other2 <= 0:
                            k += 1
                else:
                    y = [np.log(derivative_value), np.log(derivative_other1), np.log(derivative_other2)]
                    slope, intercept, _, _, _ = scipy.stats.linregress(x, y)
                    energy = -slope * 8.314
                gelPoint = {
                    'temp_id': temp_id,
                    'type': 'mid',
                    'time_min': data['time_min'],
                    'energy_storage_mod': data['energy_storage_mod'],
                    'loss_mod': data['loss_mod'],
                    'complex_viscosity': data['complex_viscosity'],
                    'loss_factor': data['loss_factor'],
                    'solidification': solidification_value,
                    'derivative_value': derivative_value,
                    'energy': energy
                }
                gelPoint_data.append(gelPoint)
                current_data_index += 1
                break
                # # 寻找相邻15min内的数据
                # data_minus_15 = rheological_data.objects.filter(formulation_id=formulation_id,
                #                                                 temperature_id=temp_id,
                #                                                 time_min__gte=data['time_min'] - 15,
                #                                                 time_min__lte=data['time_min']).values('time_s',
                #                                                                                        'time_min',
                #                                                                                        'energy_storage_mod',
                #                                                                                        'loss_mod',
                #                                                                                        'loss_factor',
                #                                                                                        'complex_viscosity').first()
                # data_plus_15 = rheological_data.objects.filter(formulation_id=formulation_id,
                #                                                temperature_id=temp_id,
                #                                                time_min__gte=data['time_min'],
                #                                                time_min__lte=data['time_min'] + 15).values('time_s',
                #                                                                                            'time_min',
                #                                                                                            'energy_storage_mod',
                #                                                                                            'loss_mod',
                #                                                                                            'loss_factor',
                #                                                                                            'complex_viscosity').order_by(
                #     '-time_min').first()
                # # 凝胶点前15分钟的固化度
                # now_index = i
                # derivative_value_minus_15 = 0
                # solidification_value_minus_15 = 0
                # while now_index > 0:
                #     if solidification_list[now_index]['time_s'] == data_minus_15['time_s']:
                #         solidification_value_minus_15 = solidification_list[now_index]['solidification']
                #         derivative_value_minus_15 = calculate_derivative(temp_related_data, now_index,
                #                                                          solidification_list[now_index][
                #                                                              'solidification'],
                #                                                          solidification_list[now_index - 1][
                #                                                              'solidification'])
                #         break
                #     else:
                #         now_index -= 1
                # gelPoint = {
                #     'temp_id': temp_id,
                #     'type': 'start',
                #     'time_min': data_minus_15['time_min'],
                #     'energy_storage_mod': data_minus_15['energy_storage_mod'],
                #     'loss_mod': data_minus_15['loss_mod'],
                #     'complex_viscosity': data_minus_15['complex_viscosity'],
                #     'loss_factor': data_minus_15['loss_factor'],
                #     'solidification': solidification_value_minus_15,
                #     'derivative_value': derivative_value_minus_15,
                # }
                # gelPoint_data.append(gelPoint)
                # # 凝胶点后15分钟的固化度
                # now_index = i
                # derivative_value_plus_15 = 0
                # solidification_value_plus_15 = 0
                # while now_index > 0:
                #     if solidification_list[now_index]['time_s'] == data_plus_15['time_s']:
                #         solidification_value_plus_15 = solidification_list[now_index]['solidification']
                #         derivative_value_plus_15 = calculate_derivative(temp_related_data, now_index,
                #                                                         solidification_list[now_index][
                #                                                             'solidification'],
                #                                                         solidification_list[now_index - 1][
                #                                                             'solidification'])
                #         break
                #     else:
                #         now_index += 1
                # gelPoint = {
                #     'temp_id': temp_id,
                #     'type': 'end',
                #     'time_min': data_plus_15['time_min'],
                #     'energy_storage_mod': data_plus_15['energy_storage_mod'],
                #     'loss_mod': data_plus_15['loss_mod'],
                #     'complex_viscosity': data_plus_15['complex_viscosity'],
                #     'loss_factor': data_plus_15['loss_factor'],
                #     'solidification': solidification_value_plus_15,
                #     'derivative_value': derivative_value_plus_15,
                # }
                # gelPoint_data.append(gelPoint)
                # current_data_index += 1
                # break
        # 寻找当前点后1000条数据的energy_storage_mod的均值
        curPoint_fileter_data = rheological_data.objects.filter(formulation_id=formulation.formulation_id,
                                                                temperature_id=temp_id).order_by('-rh_id')[
                                :1000][::-1]
        energy_storage_mod_sum = sum(data_point.energy_storage_mod for data_point in curPoint_fileter_data)
        energy_storage_mod_avg = energy_storage_mod_sum / 1000 if curPoint_fileter_data else None
        loss_mod_sum = sum(data_point.loss_mod for data_point in curPoint_fileter_data)
        loss_mod_avg = loss_mod_sum / 1000 if curPoint_fileter_data else None
        # 对比当前点的energy_storage_mod与loss_mod与后1000条数据的对应值
        threshold = 0.08
        for i, data in enumerate(temp_related_data[current_data_index + 1:len(temp_related_data) - 1000]):
            # 固化度计算
            now_index = i
            time_s_value = data['time_s']
            solidification_value = 0
            solidification_value1 = 0
            while now_index >= 0:
                if time_s_value == solidification_list[now_index]['time_s']:
                    solidification_value = solidification_list[now_index]['solidification']
                    solidification_value1 = solidification_list[now_index - 1]['solidification']
                    break
                else:
                    now_index += 1
            if (abs(data['energy_storage_mod'] - energy_storage_mod_avg) < threshold * energy_storage_mod_avg) and (
                    abs(data['loss_mod'] - loss_mod_avg) < threshold * loss_mod_avg):
                derivative_value = calculate_derivative(
                    temp_related_data[current_data_index + 1:len(temp_related_data) - 1000], i,
                    solidification_value, solidification_value1)
                derivative_other1 = 0
                derivative_other2 = 0
                j = 0
                k = 0
                # 计算表观活化能
                for j in range(len(other_list1)):
                    if abs(solidification_value - other_list1[j]['solidification'] <= 0.08 * solidification_value):
                        solid_diff = other_list1[j]['solidification'] - other_list1[j - 1]['solidification']
                        time_diff = other_list1[j]['time_s'] - other_list1[j - 1]['time_s']
                        derivative_other1 = solid_diff / time_diff
                        break
                for k in range(len(other_list2)):
                    if abs(solidification_value - other_list2[k]['solidification'] <= 0.08 * solidification_value):
                        solid_diff = other_list2[k]['solidification'] - other_list2[k - 1]['solidification']
                        time_diff = other_list2[k]['time_s'] - other_list2[k - 1]['time_s']
                        derivative_other2 = solid_diff / time_diff
                        break
                x = [(55 + 273.15) ** -1, (60 + 273.15) ** -1, (65 + 273.15) ** -1]
                energy = 0
                if energy <= 0:
                    j += 1
                    k += 1
                    now_index += 1
                    while j <= len(other_list1) and k <= len(other_list2) and now_index <= len(
                            temp_related_data[current_data_index + 1:len(temp_related_data) - 1000]):
                        solidification_value = solidification_list[now_index]['solidification']
                        solidification_value1 = solidification_list[now_index - 1]['solidification']
                        derivative_value = calculate_derivative(
                            temp_related_data[current_data_index + 1:len(temp_related_data) - 1000], i,
                            solidification_value, solidification_value1)
                        solid_diff = other_list1[j]['solidification'] - other_list1[j - 1]['solidification']
                        time_diff = other_list1[j]['time_s'] - other_list1[j - 1]['time_s']
                        derivative_other1 = solid_diff / time_diff
                        solid_diff = other_list2[k]['solidification'] - other_list2[k - 1]['solidification']
                        time_diff = other_list2[k]['time_s'] - other_list2[k - 1]['time_s']
                        derivative_other2 = solid_diff / time_diff
                        if derivative_value > 0 and derivative_other1 > 0 and derivative_other2 > 0:
                            y = [np.log(derivative_value), np.log(derivative_other1), np.log(derivative_other2)]
                            slope, intercept, _, _, _ = scipy.stats.linregress(x, y)
                            energy = -slope * 8.314
                            if energy <= 0:
                                j += 1
                                k += 1
                                now_index += 1
                            else:
                                break
                        elif derivative_value <= 0:
                            now_index += 1
                        elif derivative_other1 <= 0:
                            j += 1
                        elif derivative_other2 <= 0:
                            k += 1
                else:
                    y = [np.log(derivative_value), np.log(derivative_other1), np.log(derivative_other2)]
                    slope, intercept, _, _, _ = scipy.stats.linregress(x, y)
                    energy = -slope * 8.314
                curPoint = {
                    'temp_id': temp_id,
                    'time_min': data['time_min'],
                    'energy_storage_mod': data['energy_storage_mod'],
                    'loss_mod': data['loss_mod'],
                    'complex_viscosity': data['complex_viscosity'],
                    'loss_factor': data['loss_factor'],
                    'solidification': solidification_value,
                    'derivative_value': derivative_value,
                    'energy': energy,
                }
                curPoint_data.append(curPoint)
                break
    # 获取所有温度对象
    all_temperatures = temperature.objects.all()
    print(curPoint_data)
    # 将formulation对象转换为字典
    formulation_dict = model_to_dict(formulation)
    temperatures_json = list(all_temperatures.values())
    data = {
        'formulation': formulation_dict,
        'relatedData': sampled_data,
        'temperatures': temperatures_json,
        'gelPoint_data': gelPoint_data,
        'curPoint_data': curPoint_data,
    }
    # 将formulation、related_data和temperatures对象传递给模板进行处理
    return JsonResponse(data)


# 固化终点-模量图
def cur_Endpoint_fig(request):
    # 从数据库获取配方列表
    all_formulations = formulations.objects.all()[:9]
    all_temperatures = temperature.objects.all()
    # 构造每个配方的温度与能量储存模量的平均值数据
    data = []
    for formulation in all_formulations:
        for temp in all_temperatures:
            formulation_data = {
                'formulation_id': formulation.formulation_id,
                'temperature': 0,
                'energy_storage_mod': 0,
                'loss_mod': 0
            }
            related_data = rheological_data.objects.filter(formulation_id=formulation.formulation_id,
                                                           temperature_id=temp.temp_id).order_by('-rh_id')[:100][::-1]
            energy_storage_mod_sum = sum(data_point.energy_storage_mod for data_point in related_data)
            energy_storage_mod_avg = energy_storage_mod_sum / 100 if related_data else None
            loss_mod_sum = sum(data_point.loss_mod for data_point in related_data)
            loss_mod_avg = loss_mod_sum / 100 if related_data else None
            tp = temp.temp_value
            formulation_data['temperature'] = tp
            formulation_data['energy_storage_mod'] = energy_storage_mod_avg
            formulation_data['loss_mod'] = loss_mod_avg
            data.append(formulation_data)
    return JsonResponse(data, safe=False)


# 时间-粘度图
def time_viscosity_fig(request, formulation_id):
    # 根据formulation_id获取相应的formulations对象
    formulation = get_object_or_404(formulations, formulation_id=formulation_id)

    # 获取与该formulation_id相关的rheological_data对象
    related_data = rheological_data.objects.filter(formulation_id=formulation_id).values('rh_id', 'temperature_id_id',
                                                                                         'complex_viscosity',
                                                                                         'time_min')
    # 对related_data进行均匀抽样，每隔500条数据抽样一次
    sampled_data = []
    for i, data in enumerate(related_data):
        if i % 500 == 0:
            sampled_data.append(data)
    # 获取所有温度对象
    all_temperatures = temperature.objects.all()

    # 将formulation对象转换为字典
    formulation_dict = model_to_dict(formulation)
    temperatures_json = list(all_temperatures.values())

    data = {
        'formulation': formulation_dict,
        'relatedData': sampled_data,
        'temperatures': temperatures_json
    }
    # 将formulation、related_data和temperatures对象传递给模板进行处理
    return JsonResponse(data)


# 时间-损耗系数图
def time_loss_factor_fig(request, formulation_id):
    if request.method == 'GET':
        # 根据formulation_id获取相应的formulations对象
        formulation = get_object_or_404(formulations, formulation_id=formulation_id)

        # 获取与该formulation_id相关的rheological_data对象
        related_data = rheological_data.objects.filter(formulation_id=formulation_id).values('rh_id',
                                                                                             'temperature_id_id',
                                                                                             'loss_factor', 'time_min')
        # 获取所有温度对象
        all_temperatures = temperature.objects.all()
        # 对related_data进行均匀抽样，每隔500条数据抽样一次
        sampled_data = []
        for i, data in enumerate(related_data):
            if i % 500 == 0:
                sampled_data.append(data)
        # 将formulation对象转换为字典
        formulation_dict = model_to_dict(formulation)
        temperatures_json = list(all_temperatures.values())

        data = {
            'formulation': formulation_dict,
            'relatedData': sampled_data,
            'temperatures': temperatures_json
        }
        # 将formulation、related_data和temperatures对象传递给模板进行处理
        return JsonResponse(data)


# 时间-固化度图
def time_solidification_fig(request, formulation_id):
    if request.method == 'GET':
        formulation = get_object_or_404(formulations, formulation_id=formulation_id)
        # 获取所有温度对象
        all_temperatures = temperature.objects.all()
        solidification_data_55 = []
        solidification_data_65 = []
        solidification_data_60 = []
        for temperatures in all_temperatures:
            max_mod = rheological_data.objects.filter(
                formulation_id=formulation.formulation_id,
                temperature_id=temperatures.temp_id
            ).aggregate(max_energy_storage_mod=Max('energy_storage_mod'))['max_energy_storage_mod']
            min_mod = rheological_data.objects.filter(formulation_id=formulation_id,
                                                      temperature_id=temperatures.temp_id).values(
                'energy_storage_mod').first()['energy_storage_mod']
            related_data = rheological_data.objects.filter(formulation_id=formulation_id,
                                                           temperature_id=temperatures.temp_id).values('time_s',
                                                                                                       'temp_mark',
                                                                                                       'temperature_id',
                                                                                                       'energy_storage_mod')
            for data in related_data:
                solidification_value = (data['energy_storage_mod'] - min_mod) / (max_mod - min_mod)
                solidification = {
                    'time_s': data['time_s'],
                    'solidification': solidification_value,
                }
                if temperatures.temp_id == 1:
                    solidification_data_55.append(solidification)
                elif temperatures.temp_id == 2:
                    solidification_data_60.append(solidification)
                elif temperatures.temp_id == 3:
                    solidification_data_65.append(solidification)
        formulation_dict = model_to_dict(formulation)

        interpolated_data_55 = []
        for i, data in enumerate(solidification_data_55):
            if i % 200 == 0:
                interpolated_data_55.append(data)

        interpolated_data_60 = []
        for i, data in enumerate(solidification_data_60):
            if i % 200 == 0:
                interpolated_data_60.append(data)
        interpolated_data_65 = []
        for i, data in enumerate(solidification_data_65):
            if i % 200 == 0:
                interpolated_data_65.append(data)
        data = {
            'formulation': formulation_dict,
            'solidification_55': interpolated_data_55,
            'solidification_60': interpolated_data_60,
            'solidification_65': interpolated_data_65,

        }

        return JsonResponse(data, safe=False)


def solidification_solidDerivative_fig(request, formulation_id, window_length):
    if request.method == 'GET':
        formulation = get_object_or_404(formulations, formulation_id=formulation_id)
        # 获取所有温度对象
        all_temperatures = temperature.objects.all()
        solidification_data_55 = []
        solidification_data_65 = []
        solidification_data_60 = []
        for temperatures in all_temperatures:
            solidification_data = []
            max_mod = rheological_data.objects.filter(
                formulation_id=formulation.formulation_id,
                temperature_id=temperatures.temp_id
            ).aggregate(max_energy_storage_mod=Max('energy_storage_mod'))['max_energy_storage_mod']
            min_mod = rheological_data.objects.filter(formulation_id=formulation_id,
                                                      temperature_id=temperatures.temp_id).values(
                'energy_storage_mod').first()['energy_storage_mod']
            related_data = rheological_data.objects.filter(formulation_id=formulation_id,
                                                           temperature_id=temperatures.temp_id).values('time_s',
                                                                                                       'energy_storage_mod')
            for i, data in enumerate(related_data):
                solidification_value = (data['energy_storage_mod'] - min_mod) / (max_mod - min_mod)
                # 计算导数
                if i > 0:
                    solidification_change = solidification_value - solidification_data[-1]['solidification']
                    time_change = data['time_s'] - solidification_data[-1]['time_s']
                    if time_change != 0:
                        derivative_value = solidification_change / time_change
                    else:
                        derivative_value = 0
                else:
                    derivative_value = 0
                solidification = {
                    'time_s': data['time_s'],
                    'solidification': solidification_value,
                    'derivative_value': derivative_value
                }
                solidification_data.append(solidification)
                if temperatures.temp_id == 1:
                    solidification_data_55.append(solidification)
                elif temperatures.temp_id == 2:
                    solidification_data_60.append(solidification)
                elif temperatures.temp_id == 3:
                    solidification_data_65.append(solidification)
        formulation_dict = model_to_dict(formulation)
        # 对 solidification_55/60/65 数据进行滤波
        der_55_filtered = savgol_filter([data['derivative_value'] for data in solidification_data_55],
                                        window_length=window_length, polyorder=2)
        der_60_filtered = savgol_filter([data['derivative_value'] for data in solidification_data_60],
                                        window_length=window_length, polyorder=2)
        der_65_filtered = savgol_filter([data['derivative_value'] for data in solidification_data_65],
                                        window_length=window_length, polyorder=2)

        for i in range(len(solidification_data_55)):
            solidification_data_55[i]['derivative_value'] = der_55_filtered[i]
        for i in range(len(solidification_data_65)):
            solidification_data_65[i]['derivative_value'] = der_65_filtered[i]
        for i in range(len(solidification_data_60)):
            solidification_data_60[i]['derivative_value'] = der_60_filtered[i]

        sampled_data_55 = []
        for i, data in enumerate(solidification_data_55):
            if i % 200 == 0:
                sampled_data_55.append(data)

        sampled_data_60 = []
        for i, data in enumerate(solidification_data_60):
            if i % 200 == 0:
                sampled_data_60.append(data)
        sampled_data_65 = []
        for i, data in enumerate(solidification_data_65):
            if i % 200 == 0:
                sampled_data_65.append(data)
        print(sampled_data_60)
        print(len(sampled_data_65))
        data = {
            'formulation': formulation_dict,
            'solidification_55': sampled_data_55,
            'solidification_60': sampled_data_60,
            'solidification_65': sampled_data_65,

        }
        return JsonResponse(data, safe=False)


def ea_solidification_fig(request, formulation_id):
    if request.method == 'GET':
        formulation = get_object_or_404(formulations, formulation_id=formulation_id)
        # 获取与该formulation_id相关的rheological_data对象
        related_data = rheological_data.objects.filter(formulation_id=formulation_id).values('temperature_id_id',
                                                                                             'time_s',
                                                                                             'energy_storage_mod')

        solidification_list_60 = []
        solidification_list_55 = []
        solidification_list_65 = []
        ea_solid_list = []
        target_solidification_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7,
                                        0.8, 0.9, 0.95]
        # 计算三种温度下的固化度与固化速率
        for temp_id in set(data['temperature_id_id'] for data in related_data):
            temp_related_data = [data for data in related_data if data['temperature_id_id'] == temp_id]
            max_mod = rheological_data.objects.filter(
                formulation_id=formulation.formulation_id,
                temperature_id=temp_id
            ).aggregate(max_energy_storage_mod=Max('energy_storage_mod'))['max_energy_storage_mod']
            min_mod = rheological_data.objects.filter(formulation_id=formulation_id,
                                                      temperature_id=temp_id).values(
                'energy_storage_mod').first()['energy_storage_mod']
            for i, data in enumerate(temp_related_data):
                # 固化度计算与固化速率计算
                solidification_value = (data['energy_storage_mod'] - min_mod) / (max_mod - min_mod)
                time_s_value = data['time_s']
                if temp_id == 1:
                    if i > 0:
                        solid_diff = solidification_value - solidification_list_55[i - 1]['solidification']
                        time_s_diff = time_s_value - solidification_list_55[i - 1]['time_s']
                        derivative_value = solid_diff / time_s_diff
                        solidification_list_55.append({
                            'solidification': solidification_value,
                            'derivative_value': derivative_value,
                            'time_s': time_s_value
                        })
                    else:
                        solidification_list_55.append({
                            'solidification': solidification_value,
                            'derivative_value': 0,
                            'time_s': time_s_value
                        })
                elif temp_id == 2:
                    if i > 0:
                        solid_diff = solidification_value - solidification_list_60[i - 1]['solidification']
                        time_s_diff = time_s_value - solidification_list_60[i - 1]['time_s']
                        derivative_value = solid_diff / time_s_diff
                        solidification_list_60.append({
                            'solidification': solidification_value,
                            'derivative_value': derivative_value,
                            'time_s': time_s_value
                        })
                    else:
                        solidification_list_60.append({
                            'solidification': solidification_value,
                            'derivative_value': 0,
                            'time_s': time_s_value
                        })
                elif temp_id == 3:
                    if i > 0:
                        solid_diff = solidification_value - solidification_list_65[i - 1]['solidification']
                        time_s_diff = time_s_value - solidification_list_65[i - 1]['time_s']
                        derivative_value = solid_diff / time_s_diff
                        solidification_list_65.append({
                            'solidification': solidification_value,
                            'derivative_value': derivative_value,
                            'time_s': time_s_value
                        })
                    else:
                        solidification_list_65.append({
                            'solidification': solidification_value,
                            'derivative_value': 0,
                            'time_s': time_s_value
                        })
        flagI = 0
        flagJ = 0
        flagK = 0
        x = [(55 + 273.15) ** -1, (60 + 273.15) ** -1, (65 + 273.15) ** -1]
        for target_solid in target_solidification_values:
            derivative_value1 = 0
            derivative_value2 = 0
            derivative_value3 = 0

            i = flagI + 1
            j = flagJ + 1
            k = flagK + 1
            while i <= len(solidification_list_55):
                if abs(target_solid - solidification_list_55[i]['solidification']) <= 0.08 * target_solid:
                    derivative_value1 = solidification_list_55[i]['derivative_value']
                    flagI = i
                    break
                else:
                    i += 1
            while j <= len(solidification_list_60):
                if abs(target_solid - solidification_list_60[j]['solidification']) <= 0.08 * target_solid:
                    derivative_value2 = solidification_list_60[j]['derivative_value']
                    flagJ = j
                    break
                else:
                    j += 1
            while k <= len(solidification_list_65):
                if abs(target_solid - solidification_list_65[k]['solidification']) <= 0.08 * target_solid:
                    derivative_value3 = solidification_list_65[k]['derivative_value']
                    flagK = k
                    break
                else:
                    k += 1
            if derivative_value1 > 0 and derivative_value2 > 0 and derivative_value3 > 0:
                y = [np.log(derivative_value1), np.log(derivative_value2), np.log(derivative_value3)]
                slope, intercept, _, _, _ = scipy.stats.linregress(x, y)
                energy = -slope * 8.314
                if energy <= 0:
                    i += 1
                    j += 1
                    k += 1
                    while i <= len(solidification_list_55) and j <= len(solidification_list_60) and k <= len(
                            solidification_list_65):
                        derivative_value1 = solidification_list_55[i]['derivative_value']
                        derivative_value2 = solidification_list_60[j]['derivative_value']
                        derivative_value3 = solidification_list_65[k]['derivative_value']
                        if derivative_value1 > 0 and derivative_value2 > 0 and derivative_value3 > 0:
                            y = [np.log(derivative_value1), np.log(derivative_value2), np.log(derivative_value3)]
                            slope, intercept, _, _, _ = scipy.stats.linregress(x, y)
                            energy = -slope * 8.314
                            if energy <= 0:
                                i += 1
                                j += 1
                                k += 1
                            else:
                                flagI = i
                                flagJ = j
                                flagK = k
                                break
                        elif derivative_value1 <= 0:
                            i += 1
                        elif derivative_value2 <= 0:
                            j += 1
                        elif derivative_value3 <= 0:
                            k += 1
                        else:
                            i += 1
                            j += 1
                            k += 1
                ea_solid = {
                    'solidification': target_solid,
                    'energy': energy
                }
                ea_solid_list.append(ea_solid)
        print(ea_solid_list)

        formulation_dict = model_to_dict(formulation)
        data = {
            'formulation': formulation_dict,
            'ea_solid': ea_solid_list

        }
        return JsonResponse(data, safe=False)
