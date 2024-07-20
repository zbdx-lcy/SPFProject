from django.test import TestCase

# Create your tests here.
import pandas as pd
import pymysql
from django.db import connection, models
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from formulation.models import formulations
from .models import rheological_data
from temperature.models import temperature
from tqdm import tqdm


# 处理上传文件
def process_uploaded_file(file):
    # 读取Excel文件的所有分页
    xls = pd.ExcelFile(file)
    # 分页名称列表
    sheet_names = xls.sheet_names
    # 需要读取的列名
    column_names = ['数据点编号', '时间', '温度', '储能模量', '损耗模量', '损耗因子', '复数黏度', '间隙', '法向力', '扭矩', '状态']
    total_iterations = len(sheet_names)
    iterations = tqdm(enumerate(sheet_names, start=1), total=total_iterations, desc='Processing')
    # 遍历每个分页
    for item, sheet_name in iterations:
        print(type(sheet_name))
        formulation = formulations.objects.get(formulation_id=sheet_name)
        # 读取当前分页的数据
        df = pd.read_excel(file, sheet_name=sheet_name, usecols=column_names, engine='openpyxl')
        # 处理温度和时间数据
        df['temperature_id'] = df['温度'].apply(lambda x: get_temperature_id(x))
        temps = temperature.objects.get(temp_id=df['temperature_id'][1])
        df['temp_mark'] = df['温度'].apply(lambda x: get_temp_mark(x))
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
        for data in data_list:
            print(sheet_name, data['time_min'], data['time_s'], data['energy_storage_mod'])

# 根据温度获取温度ID
def get_temperature_id(temperature):
    if abs(temperature - 55) <= 1:
        return 1
    elif abs(temperature - 60) <= 1:
        return 2
    elif abs(temperature - 65) <= 1:
        return 3
    else:
        return 0

# 获取温度标记
def get_temp_mark(temperature):
    if abs(temperature - 55) <= 1:
        return 55
    elif abs(temperature - 60) <= 1:
        return 60
    elif abs(temperature - 65) <= 1:
        return 65
    else:
        return 0

# 在视图函数中处理上传文件
def handle_uploaded_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']

        # 保存文件到服务器
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        file_path = fs.path(filename)

        # 读取Excel文件并操作数据库
        process_uploaded_file(file_path)

        # 返回响应
        return HttpResponse('文件上传成功')
    else:
        return HttpResponse('文件上传失败')