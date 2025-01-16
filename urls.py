"""SPFProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf import settings
from .views import home
from bgfile.views import get_download_result,bgfile_download# 直接导入视图函数

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html')),
    path('formulation/', include('formulation.urls')),
    path('rhdata/', include('rhdata.urls')),
    path('users/', include('user.urls')),
    path('fileupload/', include("fileupload.urls")),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    path('', home, ),
    path('bengoumodel/', include('bengoumodel.urls')),
    path('fit/', include('fit.urls')),

    path('bengoudata/', include('bengoudata.urls')),
    path('bgfile/', include('bgfile.urls')),
    # 精确匹配 bgfile_download 路由，支持可选的空格
    re_path(r'^bgfile_download/?\s*$', bgfile_download, name='bgfile_download'),

    # 处理下载结果的路由
    # 修改下载结果路由，使用正则匹配
    re_path(r'^get_download_result/?\s*$', get_download_result, name='get_download_result'),

]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
