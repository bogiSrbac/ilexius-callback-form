from django import forms
from .models import Customer
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.core.exceptions import ValidationError


class CreateCusomerForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = Customer
        # fields = '__all__'
        exclude = ['update', 'comment', 'realized', 'administrator',]

    def __init__(self, *args, **kwargs):
        from django.forms.widgets import HiddenInput
        super(CreateCusomerForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Required field'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Required field'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'NOT required field'
        self.fields['company'].widget.attrs['placeholder'] = 'NOT required field'
        self.fields['email'].widget.attrs['placeholder'] = 'Required field'
        self.fields['subject'].widget.attrs['placeholder'] = 'Required field'
        self.fields['problem_description'].widget.attrs['cols'] = 25
        self.fields['problem_description'].widget.attrs['rows'] = 10
        self.fields['date_and_time_for_callback'].widget.attrs['placeholder'] = 'NOT required field'
        self.fields['date_and_time_for_callback'].widget.attrs['autocomplete'] = 'off'
        self.fields['submit_date_and_time'].widget = HiddenInput()






class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['first_name', 'last_name', 'email', 'subject', 'submit_date_and_time', 'date_and_time_for_callback', 'company', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(AddCommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs['cols'] = 30
        self.fields['comment'].widget.attrs['rows'] = 5
