from django.contrib import auth
from django.test import TestCase

# from accounts.models import Token
User = auth.get_user_model()


class UserModelTest(TestCase):
    def test_user_is_valid_with_email_password_and_name(self):
        user = User(email="a@b.com", name="test")
        user.set_password("1234tass")

        user.full_clean()
