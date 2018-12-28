from django.test import TestCase
from accounts.models import CustomUser

class CustomUserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('accounts/test_models is started.')
        CustomUser.objects.create(email='ishikawa@test.com', password='test1234')

    @classmethod
    def tearDownClass(cls):
        print('accounts/test_models is end.')

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


