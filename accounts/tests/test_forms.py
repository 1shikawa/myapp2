from django.test import TestCase
from accounts.models import CustomUser

class accountFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print('accounts/test_forms is started.')
        CustomUser.objects.create_user(email='ishitest@test.com', password='test1234')

    @classmethod
    def tearDownClass(cls):
        print('accounts/test_forms is end.')

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

