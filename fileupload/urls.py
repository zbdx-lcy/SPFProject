from django.urls import path
from .views import upload_chart_image, report_out, report_show, report_create

urlpatterns = [
    path('time_loss_img/image/', upload_chart_image, name='upload_chart_image'),
    path('time_mod_img/image/', upload_chart_image),
    path('curPoint_img/image/', upload_chart_image),
    path('time_cv_img/image/', upload_chart_image),
    path('time_solid_img/image/', upload_chart_image),
    path('report_create/<int:formulation_id>/<int:temperature_id>/', report_create),
    # path('report_create/', report_create),
    path('report_out/', report_out, name='report_out'),
    path('report_show/', report_show, name='report_show')
]
