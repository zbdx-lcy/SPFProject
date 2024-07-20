import math
import shutil

from django.shortcuts import render

# Create your views here.
import os
import pandas as pd
import pymysql
from django.db import connection, models
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from formulation.models import formulations
from .models import rheological_data
from temperature.models import temperature
from tqdm import tqdm
from asgiref.sync import async_to_sync 
from channels.layers import get_channel_layer
from django.shortcuts import render

import pymysql
from django.db import connection, models
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from formulation.models import formulations
from rhdata.models import rheological_data
from temperature.models import temperature
from django.conf import settings
from fileupload.models import FileContent

from paddlets.datasets import TSDataset
import shutil
import paddle
from paddlets.models.forecasting import LSTNetRegressor
from paddlets.metrics import MAE
from paddlets.utils import backtest
from paddlets.models.model_loader import load

# index
def index(request):
    if request.method == 'GET':
        return render(request, "add_rhdata.html")


progress = 0
item_progress = 0
final_progress = 0


# 处理上传文件
def process_uploaded_file(file):
    global progress, item_progress, final_progress
    output = []
    # 读取Excel文件的所有分页
    xls = pd.ExcelFile(file)
    # 分页名称列表
    sheet_names = xls.sheet_names
    # 需要读取的列名
    column_names = ['数据点编号', '时间', '温度', '储能模量', '损耗模量', '损耗因子', '复数黏度', '间隙', '法向力',
                    '扭矩', '状态']
    total_iterations = len(sheet_names)
    iterations = tqdm(enumerate(sheet_names, start=1), total=total_iterations, desc='Processing')
    # 遍历每个分页
    for item, sheet_name in iterations:
        formulation = formulations.objects.get(formulation_id=sheet_name)
        # 读取当前分页的数据
        df = pd.read_excel(file, sheet_name=sheet_name, usecols=column_names, engine='openpyxl')
        progress = (item - 1 / total_iterations) * 100
        # 检查数据库中是否已存在对应数据
        existing_data = rheological_data.objects.filter(formulation_id_id=formulation.formulation_id,
                                                        temperature_id_id=get_temperature_id(df['温度']))
        if existing_data.exists():
            output.append(
                f"数据已存在：formulation_id={formulation.formulation_id}, temperature_id={get_temperature_id(df['温度'])}")
            continue
        # 处理温度和时间数据
        df['temperature_id'] = get_temperature_id(df['温度'])
        temps = temperature.objects.get(temp_id=df['temperature_id'][1])
        df['temp_mark'] = get_temp_mark(df['温度'])
        # # 判断时间数据是否为分钟数据
        if df['时间'][0] < 1:
            # 将时间数据视为分钟数据，存储在time_min中并乘以60存储在time_s中
            df['time_min'] = df['时间'].apply(lambda x: x)
            df['time_s'] = (df.index + 1) * 10
        else:
            # 将时间数据视为秒数据，存储在time_s中并除以60存储在time_min中
            df['time_min'] = df['时间'].apply(lambda x: round(x / 60, 3))
            df['time_s'] = df['时间'].apply(lambda x: x)
        column_mapping = {
            '数据点编号': 'rh_id',
            '温度': 'temp',
            '储能模量': 'energy_storage_mod',
            '损耗模量': 'loss_mod',
            '损耗因子': 'loss_factor',
            '复数黏度': 'complex_viscosity',
            '间隙': 'clearances',
            '法向力': 'normal_force',
            '扭矩': 'torsion',
            '状态': 'state_mark',
        }
        # 替换列名
        df = df.rename(columns=column_mapping)
        df = df.drop(columns=['时间', 'rh_id'])
        # 将NaN值替换为0
        df = df.fillna(0)
        df['normal_force'] = df['normal_force'].replace('---', 0)
        # 将数据转换为字典形式的列表
        data_list = df.to_dict('records')
        total_rows = len(data_list)
        # 将数据添加到数据库
        for i, data in tqdm(enumerate(data_list), desc='Inserting', leave=False):
            data['formulation_id'] = formulation
            data['temperature_id'] = temps
            rheological_data.objects.create(**data)
            item_progress = math.ceil((i / total_rows) * 100)
    final_progress = 100
    # 保存更改到数据库
    connection.close()
    return output


# 根据温度获取温度ID
def get_temperature_id(temperature):
    avg_temperature = temperature.mean()
    if abs(avg_temperature - 55) <= 2:
        return 1
    elif abs(avg_temperature - 60) <= 2:
        return 2
    elif abs(avg_temperature - 65) <= 2:
        return 3
    else:
        return 0


# 获取温度标记
def get_temp_mark(temperature):
    avg_temperature = temperature.mean()
    if abs(avg_temperature - 55) <= 2:
        return 55
    elif abs(avg_temperature - 60) <= 2:
        return 60
    elif abs(avg_temperature - 65) <= 2:
        return 65
    else:
        return 0


def getFileUploadProgress(request):
    global progress, item_progress, final_progress
    return JsonResponse({'progress': progress, 'item_progress': item_progress, 'final_progress': final_progress})


@csrf_exempt
# Excel文件处理与数据添加
def rhdata_add(request):
    if request.method == 'POST':
        myfile = request.FILES['file']

        # 保存文件到服务器
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        file_path = fs.path(filename)

        # 读取Excel文件并操作数据库
        output = process_uploaded_file(file_path)
        if output:
            # 返回响应
            return JsonResponse({"output": output})
        else:
            return HttpResponse('文件上传成功')
    else:
        return HttpResponse('文件上传失败')


def rhdata_list(request):
    if request.method == 'GET':
        formulation_id = request.GET.get('formulation_id_id')
        temperature_value = int(request.GET.get('temperature_id_id'))
        temperature_id = 0
        msg = ''
        if temperature_value == 55:
            temperature_id = 1
        elif temperature_value == 60:
            temperature_id = 2
        elif temperature_value == 65:
            temperature_id = 3
        else:
            msg = '温度填写有误，请输入(55/60/65)'
        data = rheological_data.objects.filter(formulation_id=formulation_id, temperature_id=temperature_id)

        data_list = []
        for item in data:
            data_list.append({
                'rh_id': item.rh_id,
                'time_min': item.time_min,
                'temp': item.temp_mark,
                'energy_storage_mod': item.energy_storage_mod,
                'loss_mod': item.loss_mod,
                'loss_factor': item.loss_factor,
                'complex_viscosity': item.complex_viscosity,
                'clearances': item.clearances,
                'normal_force': item.normal_force,
                'torsion': item.torsion,
                'state_mark': item.state_mark,
            })

        return JsonResponse({'msg': msg, 'data_list': data_list}, safe=False)


# 展示预测结果与真实数据
def predicted_truth_list(request):
    if request.method == 'GET':
        formulation_id = request.GET.get('formulation_id')
        temperature_id = request.GET.get('temperature_id')
        # 从数据库中筛选出符合条件的数据
        db_data = rheological_data.objects.filter(formulation_id=formulation_id, temperature_id=temperature_id).values(
            'time_min', 'temp', 'energy_storage_mod', 'loss_mod', 'loss_factor', 'complex_viscosity')

        # 删除前10条数据
        db_data = list(db_data[10:])
        print(len(db_data))
        # 读取已存在的 Excel 文件
        static_path = os.path.join(settings.MEDIA_ROOT, "predict_output")
        excel_file_path = os.path.join(static_path, "preds_data.xlsx")

        if os.path.exists(excel_file_path):
            excel_data = pd.read_excel(excel_file_path)
            # 将 Excel 文件数据列名加上 "_p" 后缀
            excel_data.columns = [col + '_p' for col in excel_data.columns]
        else:
            return JsonResponse({'error': '预测结果文件不存在，请进行预测'}, status=500)

        # 将数据库查询的数据列名加上 "_r" 后缀
        db_data = [{col + '_r': val for col, val in item.items()} for item in db_data]
        pd_data = pd.DataFrame(db_data)
        pd_data.set_index('time_min_r', inplace=True)
        pd_excel = pd.DataFrame(excel_data)
        pd_excel.set_index('time_min_r', inplace=True)
        print(len(pd_excel))
        # 将数据库查询的数据和 Excel 文件数据按照一定的规则拼接起来
        # 这里假设你要按照时间顺序将两组数据合并，你可以根据实际需求修改这里的逻辑
        merged_data = pd.concat([pd_excel, pd_data], axis=1)
        merged_data.reset_index(inplace=True)
        print(merged_data)

        # 将合并后的数据转换为 JSON 格式
        json_data = merged_data.to_json(orient='records')

        return JsonResponse(json_data, safe=False, status=200)


# 数据获取与数据集构建/训练及文件保存
def get_data_train(request):
    if request.method == 'GET':
        formulation_id = request.GET.get('formulation_id')
        temperature_id = request.GET.get('temperature_id')
        query_set = rheological_data.objects.filter(formulation_id=formulation_id, temperature_id=temperature_id)

        # 将查询结果转换为DataFrame格式
        data = list(query_set.values())  # 将QuerySet转换为字典列表
        df = pd.DataFrame(data)

        # 构建数据集
        dataset = TSDataset.load_from_dataframe(
            df,
            time_col="rh_id",  # 假设 rh_id 是时间列
            target_cols=["energy_storage_mod", "loss_mod", "loss_factor", "complex_viscosity"],
            # observed_cov_cols=["temp", "clearances"]  # 如果有观测的协变量，可以添加到这里
        )
        # 划分训练集和验证集
        train_dataset, val_test_dataset = dataset.split(0.7)
        val_dataset, test_dataset = val_test_dataset.split(0.5)
        train_dataset.plot(add_data=[val_dataset, test_dataset], labels=['Val', 'Test'])

        in_chunk_len = int(request.GET.get('in_chunk_len'))
        out_chunk_len = int(request.GET.get('out_chunk_len'))
        batch_size = int(request.GET.get('batch_size'))
        max_epochs = int(request.GET.get('max_epochs'))
        lst = LSTNetRegressor(
            in_chunk_len=in_chunk_len,
            out_chunk_len=out_chunk_len,
            optimizer_fn=paddle.optimizer.AdamW,  # 可以设置优化器
            optimizer_params=dict(learning_rate=3e-4),  # 可以设置学习率
            batch_size=batch_size,  # 可以设置批次大小
            max_epochs=max_epochs  # 可以设置训练轮数
        )

        lst.fit(train_dataset, val_dataset)  # 开始训练

        # 创建静态文件目录的路径
        static_path = os.path.join(settings.MEDIA_ROOT, "models")

        # 检查目录是否存在，不存在则创建
        if not os.path.exists(static_path):
            os.makedirs(static_path)

        # 将模型保存到静态文件目录中
        model_path = os.path.join(static_path, "LST")

        if os.path.exists(model_path):
            shutil.rmtree(model_path)
        os.makedirs(model_path)
        lst.save(os.path.join(model_path, "model"))

        # 返回模型路径，可以在模板中使用
        output_path = os.path.join(settings.MEDIA_ROOT, "models/LST/model")
        mae = MAE()
        mae_metrics_score = backtest(
            data=val_test_dataset,
            model=lst,
            metric=mae,
            return_predicts=False
        )
        if os.path.exists(output_path):
            return JsonResponse({'msg': '模型训练成功！', 'output_path': output_path, 'mae_score': mae_metrics_score},
                                status=200)
        else:
            return JsonResponse({'msg': '模型训练失败，模型文件未保存!'}, status=500)
    else:
        return JsonResponse({'msg': '请求失败！'}, status=404)


def predict_model(request):
    if request.method == 'GET':
        formulation_id = request.GET.get('formulation_id')
        temperature_id = request.GET.get('temperature_id')
        query_set = rheological_data.objects.filter(formulation_id=formulation_id, temperature_id=temperature_id)

        # 将查询结果转换为DataFrame格式
        data = list(query_set.values())  # 将QuerySet转换为字典列表
        df = pd.DataFrame(data)

        # 构建数据集
        dataset = TSDataset.load_from_dataframe(
            df,
            time_col="rh_id",  # 假设 rh_id 是时间列
            target_cols=["energy_storage_mod", "loss_mod", "loss_factor", "complex_viscosity"],
            # observed_cov_cols=["temp", "clearances"]  # 如果有观测的协变量，可以添加到这里
        )

        lst = load(os.path.join(settings.MEDIA_ROOT, "models/LST/model"))
        mae = MAE()
        score, preds_data = backtest(
            data=dataset,
            model=lst,
            metric=mae,
            return_predicts=True)

        # 将 preds_data 转换为 DataFrame
        predictd_df = preds_data.to_dataframe()

        # 获取静态文件目录的路径
        static_path = os.path.join(settings.MEDIA_ROOT, "predict_output")

        # 检查目录是否存在，不存在则创建
        if not os.path.exists(static_path):
            os.makedirs(static_path)

        # 设置 Excel 文件路径
        excel_file_path = os.path.join(static_path, "predicted_data.xlsx")

        # 将 DataFrame 保存到 Excel 文件中
        predictd_df.to_excel(excel_file_path)
        if os.path.exists(excel_file_path):
            return JsonResponse({'msg': '预测成功！请进行预测结果下载，查看结果。'}, status=200)
        else:
            return JsonResponse({'msg': '预测失败！请重新进行预测。'},status=404)


def get_prediced_result(request):
    try:
        # 设置 Excel 文件路径
        static_path = os.path.join(settings.MEDIA_ROOT, "predict_output")
        excel_file_path = os.path.join(static_path, "predicted_data.xlsx")
        # 读取 Excel 文件内容
        with open(excel_file_path, 'rb') as excel_file:
            excel_data = excel_file.read()
        # 返回数据
        # 构造 HTTP 响应
        response = HttpResponse(excel_data,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="predicted_data.xlsx"'

        return response
    except FileNotFoundError:
        return JsonResponse({'msg': '预测失败'}, status=404)
    except Exception as e:
        return JsonResponse({'msg': '获取预测结果失败'}, status=500)
