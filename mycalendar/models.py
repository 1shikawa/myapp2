import datetime
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator, slug_re
from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
#     """カスタムユーザー"""
#     email = models.EmailField(_('email address'), unique=True)


class LargeItem(models.Model):
    """大項目"""
    name = models.CharField(verbose_name='大項目', max_length=255)

    def __str__(self):
        return self.name

class MiddleItem(models.Model):
    """中項目"""
    name = models.CharField(verbose_name='中項目', max_length=255)
    parent = models.ForeignKey(LargeItem, verbose_name='大項目', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    """スケジュール"""
    # LargeItem_choices = (
    #     ("HMK・旧シス対応", 'HMK・旧シス対応'),
    #     ("サービス対応", 'サービス対応'),
    #     ("抽出", '抽出'),
    #     ("PJT/案件", 'PJT/案件'),
    #     ("運用", '運用'),
    #     ("障害対応", '障害対応'),
    #     ("各種資料作成・入力", '各種資料作成・入力'),
    # )
    # LargeItem = models.CharField("大項目", max_length=50, blank=True, choices=LargeItem_choices)
    # LargeItem = models.CharField("大項目", max_length=50, blank=True)
    # MiddleItem = models.CharField("中項目", max_length=50, blank=True)
    LargeItem = models.ForeignKey(LargeItem, verbose_name='大項目',on_delete=models.PROTECT)
    MiddleItem = models.ForeignKey(MiddleItem,verbose_name='中項目',on_delete=models.PROTECT)
    SmallItem = models.CharField("小項目", max_length=50, blank=True)
    summary = models.CharField('概要', max_length=50,blank=True)
    description = models.TextField('詳細な説明', blank=True)
    memo = models.CharField('備考', max_length=50,blank=True)
    start_time = models.TimeField('開始時間', default=datetime.time(7, 0, 0))
    end_time = models.TimeField('終了時間', default=datetime.time(7, 0, 0))
    date = models.DateField('日付')
    kosu = models.PositiveIntegerField('時間（分）', blank=True, default=0,validators=[RegexValidator(
        slug_re,
        '時間（分）には半角英数字のみ指定できます。',
        'invalid'
    )])
    # kosu = models.CharField('時間', max_length=50,blank=True)
    totalkosu = models.PositiveIntegerField('総時間（分）', blank=True, default=0)
    register = models.CharField('登録者', max_length=50)
    created_at = models.DateTimeField('登録日時', default=timezone.now)
    updated_at = models.DateTimeField('更新日時', auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.LargeItem)

