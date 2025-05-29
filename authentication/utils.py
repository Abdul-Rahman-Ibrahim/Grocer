from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from six import text_type

class AppTokenGenerator(PasswordResetTokenGenerator):
    pass
