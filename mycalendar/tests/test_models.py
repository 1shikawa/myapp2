from django.test import TestCase

# Create your tests here.

from accounts.models import CustomUser

class CustomUserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        CustomUser.objects.create(email='ishikawa@test.com', password='test12344')

    def email_label(self):
        CustomUser=CustomUser.objects.get(id=1)
        email_label = CustomUser._meta.get_field('email').verbose_name
        self.assertEquals(email_label,'email')

    # def password_label(self):
    #     CustomUser=CustomUser.objects.get(id=1)
    #     password_label = CustomUser._meta.get_field('password').verbose_name
    #     self.assertEquals(password_label,'password')


        
