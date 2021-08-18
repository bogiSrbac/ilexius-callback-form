1.Link to Django documentation for installation on windows: https://docs.djangoproject.com/en/3.2/howto/windows/
in terminal cd path-to-ilexius-project
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
add your email, username and password

2.django-phonenumber-field:
link for installation instruction https://github.com/stefanfoulis/django-phonenumber-field

3.phonenumbers:
link for installation instructions https://github.com/daviddrysdale/python-phonenumbers

4.google reCaptcha instructions:
link https://developers.google.com/recaptcha/intro
in settings.py enetr valid two keys for recaptcha
in form I used ReCaptchaV2Checkbox

5.Django google reCaptcha:
https://pypi.org/project/django-recaptcha/

6.Argon2:
python -m pip install argon2-cffi

7.instructions for celery are in celery.py.txt file

8.django crispy forms
pip install django-crispy-forms

it is alredy added to settins.installed apps
INSTALLED_APPS = (
    ...
    'crispy_forms',
)

9.for email smtp you need to enter your gmail account in settings.py




