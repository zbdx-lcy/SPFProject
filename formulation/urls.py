from django.urls import path

from formulation import views

urlpatterns = [
    path('', views.index),
    path('formulation_upload/', views.formulation_upload),
    path('formulation_list/', views.formulation_list),
    path('formulation_del/<int:formulation_id>/', views.formulation_del),
    path('formulation_update/<int:formulation_id>/', views.formulation_update),
    path('formulation_add/', views.formulation_add),
    # 时间-模量图
    path('time_mod_fig/<int:formulation_id>/', views.time_mod_fig, name='time_mod_fig'),
    # 固化终点-模量图
    path('cur_Endpoint_fig/', views.cur_Endpoint_fig, name='cur_Endpoint_fig'),
    # 时间-粘度图
    path('time_viscosity_fig/<int:formulation_id>/', views.time_viscosity_fig),
    # 时间-损耗系数图
    path('time_loss_factor_fig/<int:formulation_id>/', views.time_loss_factor_fig),
    # 时间-固化度图
    path('time_solidification_fig/<int:formulation_id>/', views.time_solidification_fig),
    # 固化度-固化速率图
    path('solidification_derivative_fig/<int:formulation_id>/<int:window_length>/', views.solidification_solidDerivative_fig),
    # 表观活化能-固化度图
    path('ea_solidification_fig/<int:formulation_id>/', views.ea_solidification_fig),
]
