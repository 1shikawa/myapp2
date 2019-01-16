import locale
import logging
import csv
import datetime
from datetime import timedelta
from django.utils.decorators import method_decorator  # @method_decoratorに使用
from django.contrib.auth.decorators import login_required  # @method_decoratorに使用
from django.contrib import messages  # メッセージフレームワーク
from django.shortcuts import redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from mycalendar.models import Schedule, LargeItem
from accounts.models import CustomUser
from .forms import BS4ScheduleForm, BS4ScheduleNewFormSet, BS4ScheduleEditFormSet
from .basecalendar import (
    MonthCalendarMixin, MonthWithScheduleMixin
)
from django.db.models import Sum
from dateutil.relativedelta import relativedelta
import pandas as pd

locale.setlocale(locale.LC_ALL, '')
logger = logging.getLogger(__name__)


# @method_decorator(login_required, name='dispatch')
# class PasswordChange(PasswordChangeView):
#     """パスワード変更ビュー"""
#     form_class = MyPasswordChangeForm
#     success_url = reverse_lazy('mycalendar:password_change_done')
#     template_name = 'account/password_change.html'
#
#
# @method_decorator(login_required, name='dispatch')
# class PasswordChangeDone(PasswordChangeDoneView):
#     """パスワード変更後ビュー"""
#     template_name = 'account/password_change_done.html'

# クラスベースビューの場合のデコレータ
@method_decorator(login_required, name='dispatch')
class MonthWithScheduleCalendar(MonthWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの月間カレンダーを表示するビュー"""
    template_name = 'month_with_schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """月間カレンダー情報の入った辞書を返す"""
        context['month'] = self.get_month_calendar()
        logger.info("User:{} got month schecule.".format(str(self.request.user).split('@')[0]))
        return context


# 単一登録
# class NewAdd(MonthCalendarMixin,generic.CreateView):
#     template_name = 'newadd.html'
#     form_class = BS4ScheduleForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['week'] = self.get_week_calendar()
#         context['month'] = self.get_month_calendar()
#         return context
#
#     def form_valid(self, form):
#         month = self.kwargs.get('month')
#         year = self.kwargs.get('year')
#         day = self.kwargs.get('day')
#         if month and year and day:
#             date = datetime.date(year=int(year), month=int(month), day=int(day))
#         else:
#             date = datetime.date.today()
#         schedule = form.save(commit=False)
#         schedule.register = self.request.user
#         schedule.date = date
#         schedule.save()
#         return redirect('mycalendar:month_with_schedule', year=date.year, month=date.month, day=date.day)


@method_decorator(login_required, name='dispatch')
class NewMultiAdd(MonthCalendarMixin, generic.FormView):
    """一括登録・登録後表示"""
    template_name = 'multiAdd.html'
    # form_class = BS4ScheduleFormSet
    success_url = reverse_lazy('mycalendar:month_with_schedule')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['week'] = self.get_week_calendar()
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        indate = str(year) + '年' + str(month) + '月' + str(day) + '日'
        date = datetime.date(year=int(year), month=int(month), day=int(day))
        context['indate'] = indate
        context['month'] = self.get_month_calendar()
        context['LargeItem'] = LargeItem.objects.all()
        context['registered'] = Schedule.objects.filter(date=date).filter(register=str(self.request.user).split('@')[0])
        try:
            totalkosu = Schedule.objects.filter(date=date).filter(register=str(self.request.user).split('@')[0]).first()
            context['totalkosu'] = totalkosu
        except:
            context['totalkosu'] = 0
        return context

    def get_form(self, form_class=None):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = str(year) + '-' + str(month) + '-' + str(day)
        return BS4ScheduleNewFormSet(self.request.POST or None,
                                     queryset=Schedule.objects.none())

    def form_valid(self, form):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        # for fm in form:
        #     schedule = fm.save(commit=False)
        #     # schedule.register = self.request.user
        #     schedule.date = date
        #     schedule.save()
        # return redirect('mycalendar:month_with_schedule', year=date.year, month=date.month, day=date.day)
        # return super().form_valid(form)

        instances = form.save(commit=False)
        # 新たに作成されたscheduleと更新されたscheduleを取り出して、新規作成or更新処理
        for schedule in instances:
            schedule.register = str(self.request.user).split('@')[0]
            schedule.date = date
            schedule.save()
        # 総時間をkosuを合計してカラムに登録
        kosuBydate = Schedule.objects.filter(date=date).values('date', 'register').annotate(totalkosu=Sum('kosu'))
        for i in kosuBydate:
            if i['register'] == str(self.request.user).split('@')[0]:
                total = i['totalkosu']

        for row in Schedule.objects.filter(date=date).filter(register=str(self.request.user).split('@')[0]):
            row.totalkosu = int(total)
            row.save()

        logger.info("User:{} MultiAdd in {} successfully.".format(str(self.request.user), date))
        messages.success(self.request, date.strftime('%Y年%m月%d日') + "に新規登録しました。")
        # return redirect('mycalendar:month_with_schedule', year=date.year, month=date.month, day=date.day)
        return redirect('mycalendar:NewMultiAdd', year=date.year, month=date.month, day=date.day)


@method_decorator(login_required, name='dispatch')
class NewMultiEdit(MonthCalendarMixin, generic.FormView):
    """一括編集機能"""
    template_name = 'multiEdit.html'
    # form_class = BS4ScheduleFormSet
    success_url = reverse_lazy('mycalendar:month_with_schedule')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['week'] = self.get_week_calendar()
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        indate = str(year) + '年' + str(month) + '月' + str(day) + '日'
        context['month'] = self.get_month_calendar()
        context['indate'] = indate
        context['LargeItem'] = LargeItem.objects.all()
        return context

    def get_form(self, form_class=None):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = str(year) + '-' + str(month) + '-' + str(day)
        return BS4ScheduleEditFormSet(self.request.POST or None,
                                      queryset=Schedule.objects.filter(date=date,
                                                                       register=str(self.request.user).split('@')[0]))

        # def form_valid(self, form):
        #     month = self.kwargs.get('month')
        #     year = self.kwargs.get('year')
        #     day = self.kwargs.get('day')
        #     if month and year and day:
        #         date = datetime.date(year=int(year), month=int(month), day=int(day))
        #     else:
        #         date = datetime.date.today()
        #     for fm in form:
        #         schedule = fm.save(commit=False)
        #         # schedule.register = self.request.user
        #         schedule.date = date
        #         schedule.save()
        #     return redirect('mycalendar:month_with_schedule', year=date.year, month=date.month, day=date.day)
        # return super().form_valid(form)

    def form_valid(self, form):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        # instancesは、新たに作成されたscheduleと更新されたscheduleが入ったリスト
        instances = form.save(commit=False)

        # まず、削除チェックがついたscheduleを取り出して削除
        for schedule in form.deleted_objects:
            schedule.delete()

        total = 0
        # 新たに作成されたscheduleと更新されたscheduleを取り出して、新規作成or更新処理
        for schedule in instances:
            schedule.register = str(self.request.user).split('@')[0]
            schedule.date = date
            schedule.save()

        kosuBydate = Schedule.objects.filter(date=date).values('date', 'register').annotate(totalkosu=Sum('kosu'))
        for i in kosuBydate:
            if i['register'] == str(self.request.user).split('@')[0]:
                total = i['totalkosu']

        for row in Schedule.objects.filter(date=date).filter(register=str(self.request.user).split('@')[0]):
            row.totalkosu = int(total)
            row.save()
        messages.success(self.request, date.strftime('%Y年%m月%d日') + "を更新しました。")
        logger.info("User:{} MultiEdit in {} successfully.".format(str(self.request.user), date))
        return redirect('mycalendar:month_with_schedule', year=date.year, month=date.month, day=date.day)
        # return super().form_valid(form)


# class NewEdit(MonthCalendarMixin,generic.UpdateView):
#     model = Schedule
#     template_name = 'newedit.html'
#     form_class = BS4ScheduleForm
#     # success_url = reverse_lazy('mycalendar:month_with_schedule')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['week'] = self.get_week_calendar()
#         context['month'] = self.get_month_calendar()
#         return context
#
#     def form_valid(self, form):
#         month = self.kwargs.get('month')
#         year = self.kwargs.get('year')
#         day = self.kwargs.get('day')
#         if month and year and day:
#             date = datetime.date(year=int(year), month=int(month), day=int(day))
#         else:
#             date = datetime.date.today()
#         schedule = form.save(commit=False)
#         schedule.date = date
#         schedule.save()
#         return redirect('mycalendar:month_with_schedule', year=date.year, month=date.month, day=date.day)

@method_decorator(login_required, name='dispatch')
class MyCalendar(MonthCalendarMixin, generic.CreateView):
    """月間カレンダー、週間カレンダー、スケジュール登録画面のある欲張りビュー"""
    template_name = 'mycalendar.html'
    form_class = BS4ScheduleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['week'] = self.get_week_calendar()
        """月間カレンダー情報の入った辞書を返す"""
        context['month'] = self.get_month_calendar()
        return context

    def form_valid(self, form):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        schedule = form.save(commit=False)
        schedule.date = date
        schedule.save()
        return redirect('mycalendar', year=date.year, month=date.month, day=date.day)


# @method_decorator(login_required, name='dispatch')
# class inputList(generic.TemplateView):
#     """入力一覧表示"""
#     template_name = 'inputList.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['inputList'] = Schedule.objects.all().order_by('date')
#         return context

@method_decorator(login_required, name='dispatch')
class DailyInputList(generic.ListView):
    """入力一覧"""
    model = Schedule
    context_object_name = 'DailyInputList'
    template_name = 'DailyInputList.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 基準日
        today = datetime.date.today()
        # 基準日の31日前を算出
        before_31_days = today - datetime.timedelta(days=1) * 31
        # 当日から1ヶ月前までを取得
        context['DailyInputList'] = Schedule.objects.filter(date__range=(before_31_days, today)).filter(
            register=str(self.request.user).split('@')[0]).order_by('-date')
        context['InputCount'] = Schedule.objects.filter(date__range=(before_31_days, today)).filter(
            register=str(self.request.user).split('@')[0]).count()
        context['InputCountDescription'] = '直近1ヶ月'
        keyword1 = self.request.GET.get('keyword1')

        if keyword1:
            year, month = keyword1.split('-')
            # 指定年月の月初日
            first_of_month = datetime.date(int(year), int(month), 1)
            # 指定年月の月末日取得
            last_of_month = datetime.date(int(year), int(month), 1) + relativedelta(months=1) + timedelta(days=-1)
            context['DailyInputList'] = Schedule.objects.filter(date__range=(first_of_month, last_of_month)).filter(
                register=str(self.request.user)).order_by('date')
            context['InputCount'] = Schedule.objects.filter(date__range=(first_of_month, last_of_month)).filter(
                register=str(self.request.user)).count()
            context['InputCountDescription'] = '指定年月'
        logger.info("User:{} DailyInputList successfully.".format(str(self.request.user)))
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(register=str(self.request.user).split('@')[0])


@method_decorator(login_required, name='dispatch')
class DailySumList(generic.ListView):
    """日次集計一覧"""
    model = Schedule
    context_object_name = 'DailySumList'
    template_name = 'DailySumList.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 基準日
        today = datetime.date.today()
        # 基準日の31日前を算出
        before_31_days = today - datetime.timedelta(days=1) * 31
        context['DailySumList'] = Schedule.objects.select_related().filter(date__range=(before_31_days, today)).values(
            'date', 'register').annotate(DailySum=Sum('kosu')).order_by('-date')
        logger.info("User:{} DailySumList successfully.".format(str(self.request.user)))
        return context


@method_decorator(login_required, name='dispatch')
class MonthlySumList(generic.ListView):
    """月次集計一覧"""
    model = Schedule
    context_object_name = 'MonthlySumList'
    template_name = 'MonthlySumList.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword1 = self.request.GET.get('keyword1')
        keyword2 = self.request.GET.get('keyword2')

        # 年月指定がある場合の処理
        if keyword1 or keyword2:
            year, month = keyword1.split('-')
            # 指定年月の月初日
            first_of_month = datetime.date(int(year), int(month), 1)
            # 指定年月の月末日取得
            last_of_month = datetime.date(int(year), int(month), 1) + relativedelta(months=1) + timedelta(days=-1)
            # 月初から月末までのスケジュール取得
            sum_of_month = Schedule.objects.select_related().filter(
                date__range=(first_of_month, last_of_month)).filter(register__contains=keyword2)
            # 大項目と登録者ごとに合計工数算出
            context['MonthlySumList'] = sum_of_month.values('LargeItem__name', 'register').annotate(
                MonthlySum=Sum('kosu')).order_by('register', 'LargeItem')
            # 指定年月表記
            context['year_month'] = '{}～{}'.format(first_of_month.strftime('%Y年%m月%d日'),
                                                   last_of_month.strftime('%m月%d日'))

        else:
            today = datetime.date.today()
            # 今月初日付を取得
            first_of_thismonth = today + relativedelta(day=1)
            # context['MonthlySumList'] = Schedule.objects.select_related().values('date','LargeItem__name','register').annotate(MonthlySum=Sum('kosu')).order_by('register','LargeItem')
            # context['MonthlySumList'] = Schedule.objects.select_related().filter(date__range=(first_of_thismonth,today)).values('date', 'LargeItem__name','register').annotate(MonthlySum=Sum('kosu')).order_by('register', 'LargeItem')

            # 今月初から今日までのスケジュールを取得
            sum_of_thismonth = Schedule.objects.select_related().filter(date__range=(first_of_thismonth, today))
            # 外部キーの表示名をidではなく、名前にする→属性名__name
            context['MonthlySumList'] = sum_of_thismonth.values('LargeItem__name', 'register').annotate(
                MonthlySum=Sum('kosu')).order_by('register', 'LargeItem')
            context['year_month'] = '{}～{}'.format(first_of_thismonth.strftime('%Y年%m月%d日'),
                                                   today.strftime('%m月%d日'))

        logger.info("User:{} MonthlySumList successfully.".format(str(self.request.user)))
        return context


@method_decorator(login_required, name='dispatch')
class Chart(generic.ListView):
    """グラフ＆チャート表示"""
    model = Schedule
    context_object_name = 'Chart'
    template_name = 'Chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        columns = ['date', 'LargeItem', 'kosu', 'register']
        df = pd.DataFrame(columns=columns)
        # DataFrameのLargeItem_idに基づきラベル付けするためのmap
        mapped = {}
        for i in LargeItem.objects.all():
            mapped[i.id] = i.name

        for i in Schedule.objects.select_related():
            se = pd.Series([
                i.date,
                i.LargeItem_id,
                i.kosu,
                i.register
            ], columns)
            # 1行ずつDataFrameに追加
            df = df.append(se, ignore_index=True)

        # LargeItemとregisterでグループ化してkosuを合計(groupオブジェクト)→DataFrameオブジェクト化
        grouped_df = df.groupby(['LargeItem', 'register'])['kosu'].sum().reset_index()
        # LargeItemをmappedでラベル変換
        grouped_df['LargeItemLabel'] = grouped_df['LargeItem'].map(mapped)
        # 登録者、大項目で昇順ソート
        sorted_grouped_df = grouped_df.sort_values(by=["register", 'LargeItem'], ascending=True)
        # context辞書にDateFrameオブジェクト追加
        context['df'] = sorted_grouped_df
        context['register'] = sorted_grouped_df['register'].drop_duplicates().reset_index()
        return context


# 関数ベースビューの場合のデコレータ
@login_required
def SumExport(request):
    """CSV出力ダウンロード"""
    csvexport = request.GET.get('csvexport')
    if csvexport:
        response = HttpResponse(content_type='text/csv', charset='utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="SumExport.csv"'  # ファイルダウンロードを強制
        # HttpResponseオブジェクトはファイルっぽいオブジェクトなので、csv.writerにそのまま渡せる。

        year, month = csvexport.split('-')
        # 指定年月の月初日
        first_of_month = datetime.date(int(year), int(month), 1)
        # 指定年月の月末日取得
        last_of_month = datetime.date(int(year), int(month), 1) + relativedelta(months=1) + timedelta(days=-1)
        # 指定月初から月末までのスケジュール取得
        sum_of_month = Schedule.objects.select_related().filter(date__range=(first_of_month, last_of_month))
        sum_of_Designated_month = sum_of_month.values('LargeItem__name', 'register').annotate(
            MonthlySum=Sum('kosu')).order_by('register', 'LargeItem')

        writer = csv.writer(response)
        writer.writerow(['年月', '大項目', '総工数', '登録者'])
        for sum in sum_of_Designated_month:
            writer.writerow([csvexport, sum['LargeItem__name'], sum['MonthlySum'], sum['register']])
        return response

    else:
        return HttpResponse('年月を指定してください。')


@method_decorator(login_required, name='dispatch')
class Graph(generic.TemplateView):
    """指定グラフ表示"""
    model = Schedule
    context_object_name = 'Graph'
    template_name = 'Graph.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        graph1 = self.request.GET.get('graph1')
        register = self.request.GET.get('register')

        context['users'] = CustomUser.objects.all()

        if register:
            columns = ['date', 'LargeItem', 'kosu', 'register']
            df = pd.DataFrame(columns=columns)
            # DataFrameのLargeItem_idに基づきラベル付けするためのmap
            mapped = {}
            for item in LargeItem.objects.all():
                mapped[item.id] = item.name

            for i in Schedule.objects.select_related():
                se = pd.Series([
                    i.date,
                    i.LargeItem_id,
                    i.kosu,
                    i.register
                ], columns)
                # 1行ずつDataFrameに追加
                df = df.append(se, ignore_index=True)

            df = df[df['register'].str.contains(register)]
            # LargeItemとregisterでグループ化してkosuを合計(groupオブジェクト)→DataFrameオブジェクト化
            grouped_df = df.groupby(['LargeItem', 'register'])['kosu'].sum().reset_index()
            # LargeItemをmappedでラベル変換
            grouped_df['LargeItemLabel'] = grouped_df['LargeItem'].map(mapped)
            # 登録者、大項目で昇順ソート
            sorted_grouped_df = grouped_df.sort_values(by=["register", 'LargeItem'], ascending=True)
            # context辞書にDateFrameオブジェクト追加
            context['df'] = sorted_grouped_df
            context['register'] = sorted_grouped_df['register'].drop_duplicates().reset_index()
            return context

        else:
            context['Graph'] = '登録者(ユーザーID)を指定してください。'
            return context


from django_datatables_view.base_datatable_view import BaseDatatableView
from excel_response import ExcelMixin


# DataTablesにデータを提供するWebAPI
# django-datatables-view
# https://pypi.org/project/django-datatables-view/
class ScheduleJsonView(BaseDatatableView):
    # モデルの指定
    model = Schedule
    # フィールドの指定
    columns = ['id', 'LargeItem', 'MiddleItem', 'SmallItem', 'date', 'kosu', 'register']

    # 検索方法の指定：部分一致
    def get_filter_method(self):
        return super().FILTER_ICONTAINS


# 印刷・Excel・CSV出力の基底クラス
class BaseReportView(generic.ListView):
    model = Schedule

    # 選択データの取得
    def get_queryset(self):
        id_list = self.request.GET['id_list'].split('_')
        result = Schedule.objects.filter(id__in=id_list)
        return result


# 印刷画面表示
class PrintView(BaseReportView):
    template_name = 'print.html'

# Excelダウンロード
# django-excel-response
# https://pypi.org/project/django-excel-response/
class ExcelView(ExcelMixin, BaseReportView):

    # 見出し行を日本語にする
    def get_queryset(self):
        header = [['id', '大項目', '中項目', '小項目', '概要', '詳細な説明', '備考', '開始時間', '終了時間', '日付', '時間（分）', '総時間（分）', '登録者']]
        body = [list(entry.values()) for entry in super().get_queryset().values()]
        return header + body


# CSVダウンロード
class CsvView(ExcelView):
    force_csv = True
