import os

import reportlab.pdfbase.ttfonts
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from SPFProject import settings
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# 在初始化canvas之前加载字体文件
# tem = reportlab.pdfbase.ttfonts.TTFont('song', 'simsun.ttc')
pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('song', 'simsun.ttc'))
pdfmetrics.registerFont(TTFont('song', 'simsun.ttf'))


@csrf_exempt
@require_POST
def upload_chart_image(request):
    if request.method == 'POST' and request.FILES.get('chartImage'):
        # 从请求中获取图像数据和文件名
        chart_image = request.FILES['chartImage']
        # 将图像数据保存到media/files目录下
        # 生成保存图像的文件路径
        file_path = os.path.join(settings.MEDIA_ROOT, 'chart_images', chart_image.name)
        try:
            # 将图像文件保存到指定路径
            with open(file_path, 'wb') as f:
                for chunk in chart_image.chunks():
                    f.write(chunk)

            return JsonResponse({'msg': '上传成功'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # 请求方法不正确或未找到图像文件时返回错误响应
        return JsonResponse({'msg': '图像文件上传失败'}, status=500)


def report_create(request, formulation_id, temperature_id):
    # formulation_id = request.GET.get('formulation_id')
    # temperature_id = request.GET.get('temperature_id')
    filename = f'FORMULATION_REPORT_{formulation_id}_{temperature_id}.pdf'
    filepath = os.path.join(settings.MEDIA_ROOT, 'files', f'{filename}')

    print(filepath)
    # if os.path.exists(filepath):
    #     return JsonResponse({'msg': '报告已存在！', 'file_path': filepath}, status=200)
    try:
        # 创建PDF文件
        c = canvas.Canvas(filepath, pagesize=letter)
        c.setFont('song', 16)
        # 写入配方编号和温度
        c.drawString(100, 750, str(f'配方编号: {formulation_id}'))
        c.drawString(100, 730, str(f'温度: {temperature_id}'))
        # 插入图表及标题
        chart_titles = [
            "时间-模量图",
            "时间-损失因子图",
            "时间-复数黏度图",
            "固化终点-储能模量图",
            "固化终点-损失模量图",
            '时间-固化度图',
            '固化度-固化速率图',
            '表观活化能-固化度图'
        ]
        chart_paths = [
            os.path.join(settings.MEDIA_ROOT, 'chart_images',
                         f'TimeModChart_{formulation_id}_{temperature_id}.png'),
            os.path.join(settings.MEDIA_ROOT, 'chart_images',
                         f'TimeLossFactorChart_{formulation_id}_{temperature_id}.png'),
            os.path.join(settings.MEDIA_ROOT, 'chart_images', f'TimeCVChart_{formulation_id}_{temperature_id}.png'),
            os.path.join(settings.MEDIA_ROOT, 'chart_images', 'CureEndpointEMModChart.png'),
            os.path.join(settings.MEDIA_ROOT, 'chart_images', 'CureEndpointLMModChart.png'),
            os.path.join(settings.MEDIA_ROOT, 'chart_images', f'TimeSolidificationChart_{formulation_id}.png'),
            os.path.join(settings.MEDIA_ROOT, 'chart_images', f'SolidDerivativeChart_{formulation_id}.png'),
            os.path.join(settings.MEDIA_ROOT, 'chart_images', f'SolidEAChart_{formulation_id}.png'),
        ]
        y_position = 500
        for title, path in zip(chart_titles, chart_paths):
            if y_position < 250:
                c.showPage()  # 创建新页面
                c.setFont('song', 16)
                c.drawString(100, 750, str(f'配方编号: {formulation_id}'))
                c.drawString(100, 730, str(f'温度: {temperature_id}'))
                y_position = 500  # 重置y_position为新页面的起始位置
            c.drawImage(ImageReader(path), 100, y_position - 20, width=400, height=200)
            y_position -= 250
        # 保存PDF文件
        c.save()
        return JsonResponse({'msg': '报告生成成功!', 'file_path': filepath}, status=200)
    except Exception as e:
        return JsonResponse({'error': '报告生成失败!', 'details': str(e)}, status=500)


def report_out(request):
    try:
        formulation_id = request.GET.get('formulationId')
        temperature_id = request.GET.get('temperatureId')
        # 根据formulation_id和temperature_id进行逻辑处理，获取对应的PDF文件名
        pdf_name = f"FORMULATION_REPORT_{formulation_id}_{temperature_id}.pdf"

        pdf_path = os.path.join(settings.MEDIA_ROOT, 'files', pdf_name)
        print(pdf_path)
        # 从本地文件系统中打开PDF文件
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{os.path.basename(pdf_path)}"'
        return response
    except Exception as e:
        return JsonResponse({'msg': '报告数据获取失败!'}, status=500)


def report_show(request):
    pdf_url = request.GET.get('url')

    # 从本地文件系统中打开PDF文件
    with open(pdf_url, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(pdf_url)}"'

    return response
