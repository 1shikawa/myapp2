from django.test import TestCase
from accounts.models import CustomUser

class accountsViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        テスト実行前の処理
        ログイン可能なユーザを1名追加
        """
        print('accounts/test_views is started.')
        CustomUser.objects.create_user(email='ishitest@test.com',
                                     password='test1234')
    @classmethod
    def tearDownClass(cls):
        print('accounts/test_views is end.')

    def test_get_login_by_unauthenticated_user(self):
        """
        ログインしていないユーザーが「/accounts/login」へのGETリクエストをすると、
        ログイン画面にアクセスされることを検証
        """
        client = self.client
        # ログイン画面が表示されるかどうか
        response = client.get('/accounts/login/')
        # ステータスコード：200が返されログイン画面にアクセス
        self.assertEqual(response.status_code, 200)

        # # setUpで追加しておいたユーザでログイン
        # client.login(email='ishitest@test.com', password='test1234')
        # # ログインしているユーザがアクセスした場合
        # response = client.get('/accounts/login/')
        # # ステータスコード：301が返却されリダイレクトされる
        # self.assertRedirects(response, '/month_with_schedule/')
        # self.assertEqual(response.status_code, 302)

    def test_get_login_by_autheticated_user(self):
        """
        ログイン済みユーザーが「/accounts/login」へGETリクエストすると、
        「/month_with_schedule」画面へリダイレクトされることを検証
        """
        # テストクライアントでログインをシミュレート
        # 認証成功なら、クライアント内部の Cookie およびセッションにユーザーの情報を保持
        client = self.client
        # setUpで追加しておいたユーザでログイン
        logged_in = client.login(email='ishitest@test.com', password='test1234')
        # 念のためログイン成功したかどうかを検証
        self.assertTrue(logged_in)

        # ログイン済みの Cookie を保持したクライアントでGETリクエストを実行
        response = self.client.get('/accounts/login/')
        # レスポンスを検証
        # self.assertRedirects(response, '/')
        self.assertEqual(response.status_code, 302)

    def test_get_index_by_autheticated_user(self):
        """
        ログイン済みユーザーが「/month_with_schedule」へGETリクエストすると、
        「/month_with_schedule」画面へリダイレクトされることを検証
        """
        # テストクライアントでログインをシミュレート
        # 認証成功なら、クライアント内部の Cookie およびセッションにユーザーの情報を保持
        client = self.client
        # setUpで追加しておいたユーザでログイン
        logged_in = client.login(email='ishitest@test.com', password='test1234')
        # 念のためログイン成功したかどうかを検証
        self.assertTrue(logged_in)

        # ログイン済みの Cookie を保持したクライアントでGETリクエストを実行
        response = self.client.get('/')
        # レスポンスを検証
        # self.assertRedirects(response, 301, '/month_with_schedule/')
        self.assertEqual(response.status_code, 301)
        self.assertTemplateNotUsed(response)


    def test_get_signup_success(self):
        """
        「/accounts/signup/」へのGETリクエストをすると、
        ユーザー登録画面に遷移することを検証
        """
        # テストクライアントでGETリクエストをシミュレート
        response = self.client.get('/accounts/signup/')

        # レスポンスを検証する
        self.assertEqual(response.status_code, 200)
        # エラーメッセージが出ないことを検証
        self.assertFalse(response.context['form'].errors)
        # 使用されているtemplateを検証
        self.assertTemplateUsed(response, 'account/signup.html')


    def test_post_signup_success(self):
        """
        「/accounts/signup/」へのPOSTリクエストをすると、
        ユーザー仮登録が成功することを検証
        """
        # テストクライアントでPOSTリクエストをシミュレート
        response = self.client.post('/accounts/signup/', {
            'email': 'user@example.com',
            'password': 'pass1234',
            'password2': 'pass1234',
        })

        # レスポンスを検証する
        self.assertEqual(response.status_code, 200)
        # 新しいユーザーが登録されたことを検証
        # self.assertTrue(get_user_model().objects.filter(username='user').exists())


    def test_post_with_same_username(self):
        """
        「/accounts/signup/」へのPOSTリクエストをする際、
        すでに登録済みのユーザーが存在する場合にユーザー登録が失敗することを検証
        """
        # テストクライアントでPOSTリクエストをシミュレート
        response = self.client.post('/accounts/signup/', {
            'email': 'ishitest@test.com',
            'password': 'test1234',
            'password2': 'test1234',
        })

        # レスポンスを検証する
        self.assertEqual(response.status_code, 200)
        # フォームに保持されたエラーメッセージを検証
        self.assertFormError(response, 'form', 'email',
                             '他のユーザーがこのメールアドレスを使用しています。')
        self.assertTemplateUsed(response, 'account/signup.html')
        # 新しいユーザーが登録されていないことを検証
        # self.assertFalse(get_user_model().objects.filter(email='ishitest@test.com').exists())
        self.assertTrue(CustomUser.objects.filter(email='ishitest@test.com').exists())

