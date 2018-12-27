from django.test import TestCase

# Create your tests here.

from accounts.models import CustomUser


class CustomUserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create(email='ishikawa@test.com', password='test1234')

    def test_email_label(self):
        user1 = CustomUser.objects.get(id=1)
        email_label = user1._meta.get_field('email').verbose_name
        self.assertEquals(email_label, 'メールアドレス')

    def test_email_value(self):
        user1 = CustomUser.objects.get(id=1)
        email_value = user1.email
        self.assertEqual(email_value, 'ishikawa@test.com')

    def test_password_label(self):
        user1 = CustomUser.objects.get(id=1)
        password_label = user1._meta.get_field('password').verbose_name
        self.assertEquals(password_label, 'パスワード')

    def test_password_value(self):
        user1 = CustomUser.objects.get(id=1)
        password_value = user1.password
        self.assertEqual(password_value, 'test1234')


from mycalendar.models import LargeItem


class LargeItemTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        LargeItem.objects.create(name='大項目テスト')

    def test_LargeItem_label(self):
        LargeItem1 = LargeItem.objects.get(id=1)
        LargeItem1_label = LargeItem1._meta.get_field('name').verbose_name
        self.assertEquals(LargeItem1_label, '大項目')

    def test_LargeItem_value(self):
        LargeItem1 = LargeItem.objects.get(id=1)
        LargeItem1_value = LargeItem1.name
        self.assertEqual(LargeItem1_value, '大項目テスト')


from mycalendar.models import MiddleItem


class MiddleItemTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        LargeItem.objects.create(name='大項目テスト')
        MiddleItem.objects.create(name='中項目テスト', parent_id='1')

    def test_MiddleItem_label(self):
        MiddleItem1 = MiddleItem.objects.get(id=1)
        MiddleItem1_label = MiddleItem1._meta.get_field('name').verbose_name
        self.assertEquals(MiddleItem1_label, '中項目')

    def test_MiddleItem_value(self):
        MiddleItem1 = MiddleItem.objects.get(id=1)
        MiddleItem1_value = MiddleItem1.name
        self.assertEqual(MiddleItem1_value, '中項目テスト')


from mycalendar.models import Schedule
from django.utils import timezone
import datetime


class ScheduleModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        LargeItem.objects.create(name='大項目テスト')
        MiddleItem.objects.create(name='中項目テスト', parent_id='1')
        Schedule.objects.create(LargeItem_id='1', MiddleItem_id='1', SmallItem='SmallItem1', kosu='99', totalkosu='99',
                                date=datetime.date(2018, 12, 31), register='ishikawa', created_at=timezone.now())

    def test_Schedule_SmallItem_label(self):
        schedule1 = Schedule.objects.get(id=1)
        schedule1_label = schedule1._meta.get_field('SmallItem').verbose_name
        self.assertEquals(schedule1_label, '小項目')

    def test_Schedule_register_label(self):
        schedule1 = Schedule.objects.get(id=1)
        schedule1_label = schedule1._meta.get_field('register').verbose_name
        self.assertEquals(schedule1_label, '登録者')

    def test_Schedule_date_label(self):
        schedule1 = Schedule.objects.get(id=1)
        schedule1_label = schedule1._meta.get_field('date').verbose_name
        self.assertEquals(schedule1_label, '日付')

    def test_Schedule_value_LargeItem(self):
        schedule1 = Schedule.objects.get(id=1)
        schedule1_value_LargeItem_id = schedule1.LargeItem_id
        self.assertEqual(schedule1_value_LargeItem_id, 1)

    def test_Schedule_value_MiddleItem(self):
        schedule1 = Schedule.objects.get(id=1)
        schedule1_value_MiddleItem_id = schedule1.MiddleItem_id
        self.assertEqual(schedule1_value_MiddleItem_id, 1)

    def test_Schedule_value_SmallItem(self):
        schedule1 = Schedule.objects.get(id=1)
        schedule1_value_SmallItem = schedule1.SmallItem
        self.assertEqual(schedule1_value_SmallItem, 'SmallItem1')

    def test_Schedule_value_register(self):
        schedule1 = Schedule.objects.get(id=1)
        schedule1_value_register = schedule1.register
        self.assertEqual(schedule1_value_register, 'ishikawa')

    def test_Schedule_value_date(self):
        schedule1 = Schedule.objects.get(id=1)
        schedule1_value_date = schedule1.date
        self.assertEqual(schedule1_value_date, datetime.date(2018, 12, 31))

