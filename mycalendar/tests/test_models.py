from django.test import TestCase
from mycalendar.models import LargeItem

class LargeItemTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('mycalendar/test_models_LargeItemTest is started.')
        LargeItem.objects.create(name='大項目テスト')

    @classmethod
    def tearDownClass(cls):
        print('mycalendar/test_models_LargeItemTest is end.')

    def test_LargeItem_label(self):
        """
        LargeItemモデルのラベルを検証
        """
        LargeItem1 = LargeItem.objects.get(id=1)
        LargeItem1_label = LargeItem1._meta.get_field('name').verbose_name
        self.assertEquals(LargeItem1_label, '大項目')

    def test_LargeItem_value(self):
        """
        登録済みのLargeItemデータを検証
        """
        LargeItem1 = LargeItem.objects.get(id=1)
        LargeItem1_value = LargeItem1.name
        self.assertEqual(LargeItem1_value, '大項目テスト')


from mycalendar.models import MiddleItem

class MiddleItemTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('mycalendar/test_models_MiddleItemTest is started.')
        LargeItem.objects.create(name='大項目テスト')
        MiddleItem.objects.create(name='中項目テスト', parent_id='1')

    @classmethod
    def tearDownClass(cls):
        print('mycalendar/test_MiddleItemTest is end.')

    def test_MiddleItem_label(self):
        """
        MiddleItemモデルのラベルを検証
        """
        MiddleItem1 = MiddleItem.objects.get(id=1)
        MiddleItem1_label = MiddleItem1._meta.get_field('name').verbose_name
        self.assertEquals(MiddleItem1_label, '中項目')

    def test_MiddleItem_value(self):
        """
        登録済みのMiddleItemデータを検証
        """
        MiddleItem1 = MiddleItem.objects.get(id=1)
        MiddleItem1_value = MiddleItem1.name
        self.assertEqual(MiddleItem1_value, '中項目テスト')


from mycalendar.models import Schedule
from django.utils import timezone
import datetime


class ScheduleModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('mycalendar/test_models_ScheduleModelTest is started.')
        LargeItem.objects.create(name='大項目テスト')
        MiddleItem.objects.create(name='中項目テスト', parent_id='1')
        Schedule.objects.create(LargeItem_id='1', MiddleItem_id='1', SmallItem='SmallItem1', kosu='99', totalkosu='99',
                                date=datetime.date(2018, 12, 31), register='ishikawa', created_at=timezone.now())

    @classmethod
    def tearDownClass(cls):
        print('mycalendar/test_models_ScheduleModelTest is end.')


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

