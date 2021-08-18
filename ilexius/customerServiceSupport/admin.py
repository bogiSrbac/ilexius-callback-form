from django.contrib import admin
from .models import Customer, Administrator, Archive


admin.site.register(Customer)
admin.site.register(Administrator)
admin.site.register(Archive)
