from django.test import TestCase
from mycalendar.models import Schedule,AuthUser

@python_2_unicode_compatible
class mycalendarViewTests(TestCase):  #AppName1は自身の環境に併せて変更してください
    def schedule(selfs):
        sh = Schedule.objects.aii()
        self.assertEqual(sh.count(), 0)

    def setUp(self):
        """
        テスト実行前の処理
        ログイン可能なユーザを1名追加しておきます
        """
        AuthUser.objects.create_user(username='test',
                                     password='test1234')

    def test_index(self):
        """
        indexの画面へアクセスできるかどうかをテストする
        この画面はログインしているユーザ出ないとアクセスできません
        """
        client = self.client

        # まずはログインしていないユーザがアクセスした場合
        response = client.get('/')
        # ステータスコード：302が返却され画面にアクセスできない
        self.assertEqual(response.status_code, 302)

        # setUpで追加しておいたユーザでログインします
        client.login(username='test', password='test1234')

        # ログインしているユーザがアクセスした場合
        response = client.get('/')
        # ステータスコード：200が返却され画面にアクセスできている
        self.assertEqual(response.status_code, 200)