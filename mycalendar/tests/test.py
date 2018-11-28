from django.test import TestCase
from mycalendar.models import Schedule
from accounts.models import CustomUser

# @python_2_unicode_compatible
class mycalendarViewTests(TestCase):
    @classmethod
    def schedule(self):
        """
        登録データはなし
        """
        sh = Schedule.objects.all().count()
        self.assertEqual(sh,200)

    def setUp(self):
        """
        テスト実行前の処理
        ログイン可能なユーザを1名追加
        """
        CustomUser.objects.create_user(email='ishitest@test.com',
                                     password='test1234')

    def test_index(self):
        """
        indexの画面へアクセスできるかどうかをテストする
        この画面はログインしているユーザでないとアクセス不可
        """
        client = self.client

        # ログイン画面が表示されるかどうか
        response = client.get('/accounts/login/')
        # ステータスコード：200が返却され画面にアクセスできる
        self.assertEqual(response.status_code, 200)

        # setUpで追加しておいたユーザでログイン
        client.login(email='ishitest@test.com', password='test1234')
        # ログインしているユーザがアクセスした場合
        response = client.get('/')
        # ステータスコード：301が返却されリダイレクトされる
        self.assertEqual(response.status_code, 301)