from django.contrib import admin
from myapp import models
# Register your models here.

admin.site.register(models.Health)
admin.site.register(models.Customer)
admin.site.register(models.Content)