from django.urls import path

from rhdata import views

urlpatterns = [
    path('', views.index),
    path('rhdata_add/', views.rhdata_add),
    path('rhdata_list/', views.rhdata_list),
    path('rhdata_Upload_Progress/', views.getFileUploadProgress),
    path('get_predicted_result/', views.get_prediced_result),
    path('process_predict/', views.predict_model),
    path('process_train/', views.get_data_train),
    path('truth_predicted_list/', views.predicted_truth_list),
]
