#from events import GenderRestriction
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image


class GenderRestriction(models.Model):
    name = models.CharField('name of gender', max_length=7)

    def __str__(self):
        return self.name


class MyAccountManager(BaseUserManager):
    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError("Вы должны ввести номер телефона")
        
        user = self.model(
            phone=phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):
        user = self.create_user(
            phone=phone,
            password= password,
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email = models.EmailField('email', max_length=60)
    phone = PhoneNumberField('phone number',max_length=12, null=False, blank=False, unique=True)
    username = None #models.CharField('username', max_length=30, unique=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    last_login = models.DateTimeField('last login ', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField('Name', max_length=30)
    second_name = models.CharField('2ndName', max_length=30)
    birth_date = models.DateField("birth date", null=True)
    sex = models.ForeignKey(GenderRestriction, on_delete=models.PROTECT, null=True, blank=True)
    country = models.CharField('country', max_length=30)
    city = models.CharField('city', max_length=30)
    profile_status = models.CharField('status', max_length=100)
    user_avatar = models.ImageField ('profile photo',default="default/default.jpg", upload_to='profile_image', blank=True)

    USERNAME_FIELD = 'phone'


    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    def __str__(self):
        return self.phone.as_e164
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

  #  def save(self):
  #      super().save()
#
#        user_avatar = Image.open(self.image.path)
#
#        if user_avatar.height > 300 or user_avatar.width > 300:
#            output_size = (300,300)
#            user_avatar.thumbnail(output_size)
#            user_avatar.save()


