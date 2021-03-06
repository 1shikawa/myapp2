from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView
from accounts.forms import ContactForm
from django.contrib.auth import views as auth_views  # ログアウトに必要

app_name = 'mycalendar'

urlpatterns = [
    path(
        'month_with_schedule/',
        views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'
    ),
    path(
        'month_with_schedule/<int:year>/<int:month>/',
        views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'
    ),
    path(
        'month_with_schedule/<int:year>/<int:month>/<int:day>',
        views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'
    ),

    # 新規単一登録
    # path(
    #     'month_with_schedule/newadd/<int:year>/<int:month>/<int:day>',
    #     views.NewAdd.as_view(), name='NewAdd'
    # ),

    # 複数登録
    path(
        'month_with_schedule/NewMultiAdd/<int:year>/<int:month>/<int:day>',
        views.NewMultiAdd.as_view(), name='NewMultiAdd'
    ),
    # 編集
    # path(
    #     'month_with_schedule/newedit/<int:pk>',
    #     views.NewEdit.as_view(), name='NewEdit'
    # ),

    # path(
    #     'month_with_schedule/newedit/<int:year>/<int:month>/<int:day>',
    #     views.NewEdit.as_view(), name='NewEdit'
    # ),
    path(
        'month_with_schedule/NewMultiEdit/<int:year>/<int:month>/<int:day>',
        views.NewMultiEdit.as_view(), name='NewMultiEdit'
    ),
    # 入力一覧
    path(
        'DailyInputList/', views.DailyInputList.as_view(), name='DailyInputList'
    ),

    # 日次集計
    path(
        'DailySumList/', views.DailySumList.as_view(), name='DailySumList'
    ),

    # 月次集計
    path(
        'MonthlySumList/', views.MonthlySumList.as_view(), name='MonthlySumList'
    ),

    # チャート
    path(
        'Chart/', views.Chart.as_view(), name='Chart'
    ),

    # 個別グラフ
    path(
        'Graph/', views.Graph.as_view(), name='Graph'
    ),

    # プロフィール
    path(
        'profile/<int:pk>', views.ProfileView.as_view(), name='profile'
    ),

    path(
        'profile/<int:pk>/update/', views.ProfileUpdateView.as_view(), name='profile_update'
    ),

    # お問い合わせ
    path(
        'contact/', views.Contact(ContactForm), name='contact'
    ),

    # path(
    #     'contact/', views.Contact, name='contact'
    # ),

    path(
        'contact_confirm', views.ContactConfirm.as_view(), name='contact_confirm'
    ),
    path(
        'contact_send', views.ContactSend.as_view(), name='contact_send'
    ),

    # CSVエクスポート
    path(
        'SumExport/', views.SumExport, name='SumExport'
    ),

    path('mycalendar/', views.MyCalendar.as_view(), name='mycalendar'),
    path(
        'mycalendar/<int:year>/<int:month>/<int:day>/', views.MyCalendar.as_view(), name='mycalendar'
    ),

    # dataTable機能
    path('datatable', TemplateView.as_view(template_name='datatable.html'), name='datatable'),
    path('schedule', views.ScheduleJsonView.as_view(), name='ScheduleJson'),
    path('print', views.PrintView.as_view(), name='print'),
    path('excel', views.ExcelView.as_view(), name='excel'),
    path('csv', views.CsvView.as_view(), name='csv'),
]
