from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from .utils import send_activation_code



class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, phone, **kwargs):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)  #переводим все в нижний регистр
        user = self.model(email=email, phone=phone, **kwargs)
        # self.model - User
        user.set_password(password)  # это у нас хеширование пароля
        user.create_activation_code() # генерируем ак/код
        send_activation_code(user.email, user.activation_code) #отправляем на почту
        user.save(using=self._db)  # сохраняем юзера в базу данных
        return user  # сохраняем юзера

    # super_user имеет доступ к админке
    def create_superuser(self, email, password, phone, **kwargs):
        if not email:
            raise ValueError('Email is required')
        kwargs["is_staff"] = True
        kwargs["is_superuser"] = True
        kwargs["is_active"] = True
        email = self.normalize_email(email)  # переводим все в нижний регистр
        user = self.model(email=email, phone=phone, **kwargs)
        # self.model - User
        user.set_password(password)  # это у нас хеширование пароля
        user.create_activation_code() # генерируем ак/код
        send_activation_code(user.email, user.activation_code) #отправляем на почту
        user.save(using=self._db)  # сохраняем юзера в базу данных
        return user  # сохраняем юзера):


class User(AbstractUser):
    username = None  # убираем username из полей
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    bio = models.TextField()
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=8, blank=True)

    USERNAME_FIELD = 'email' # логинемся через username_field
    REQUIRED_FIELDS = ['phone']

    objects = UserManager()  # обязательно указываем менеджера


    def create_activation_code(self):
        from django.utils.crypto import get_random_string
        code = get_random_string(length=8)
        self.activation_code = code
        self.save()
