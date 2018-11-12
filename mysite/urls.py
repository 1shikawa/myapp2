"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings

# 管理画面表示名変更
admin.site.site_title = 'タイトルタグ' 
admin.site.site_header = 'アプリ管理サイト' 
admin.site.index_title = 'メニュー'


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')), 認証関連ビュー有効化
    path('accounts/', include('allauth.urls')),  # Django-allauth利用
    path('', include('mycalendar.urls', namespace='mycalendar')), 
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        path('', include('mycalendar.urls', namespace='mycalendar')),
    ] + urlpatterns
