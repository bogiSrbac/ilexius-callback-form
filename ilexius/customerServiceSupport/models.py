from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime, date
import datetime
from django.utils import timezone


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Enter email address')
        if not username:
            raise ValueError('Enter your username')


        user = self.model(
            email=self.normalize_email(email),
            username=username,

        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Administrator(AbstractBaseUser):
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField( auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    year_of_birth = models.DateField(blank=True, null=True,)
    birth_place = models.CharField(max_length=50, blank=True, null=True,)
    address = models.CharField(max_length=50, blank=True, null=True,)
    zip_code = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50, blank=True, null=True,)
    cell_phone_number = models.CharField(max_length=50, blank=True, null=True)
    fax = models.CharField(max_length=50, blank=True, null=True)
    web_stranica = models.URLField(blank=True, null=True)




    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Customer(models.Model):
    first_name = models.CharField(max_length=256, blank=False)
    last_name = models.CharField(max_length=256, blank=False)
    phone_number = PhoneNumberField(blank=True, null=True, help_text='Phone number format for Serbia: </br>xxx xxx xxx or</br> xxx xxx xxxx')
    company = models.CharField(max_length=256, blank=True, null=True)
    email = models.EmailField(max_length=60, blank=False)
    subject = models.CharField(max_length=256, blank=False,)
    problem_description = models.TextField(blank=False)
    date_and_time_for_callback = models.DateTimeField(blank=True, null=True, help_text='Workdays from 08:00 to 20:00. </br> Saturday from 08:00 to 13:00.')
    submit_date_and_time = models.DateTimeField(blank=True, null=True,)
    update = models.DateTimeField(blank=True, null=True, default=datetime.datetime.now())
    comment = models.TextField(blank=True, null=True, default='Enter comment', help_text='Enter your comment as administrator.')
    realized = models.BooleanField(default=False, blank=True, null=True)
    administrator = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        first_name = self.first_name.lower()
        self.first_name = first_name.title()
        last_name = self.last_name.lower()
        self.last_name = last_name.title()
        self.update = datetime.datetime.now()
        email = self.email.lower()
        self.email = email
        return super(Customer, self).save(*args, **kwargs)

    class Meta:
        ordering = ['date_and_time_for_callback', 'submit_date_and_time', ]
#         I done it in this way because of primary callbacks term ordering. oposite would by firs according to submit




class Archive(models.Model):

    realizedCallbacks = models.ForeignKey(Customer, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        first_name = self.realizedCallbacks.first_name.lower()
        self.realizedCallbacks.first_name = first_name.title()
        last_name = self.realizedCallbacks.last_name.lower()
        self.realizedCallbacks.last_name = last_name.title()
        self.update = datetime.datetime.now()
        return super(Archive, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.realizedCallbacks)

    class Meta:
        ordering = ['realizedCallbacks__date_and_time_for_callback', 'realizedCallbacks__submit_date_and_time',]

