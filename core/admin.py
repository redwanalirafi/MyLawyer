from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Profile)
admin.site.register(HireRequest)
admin.site.register(LawyerProfile)
admin.site.register(Message)
admin.site.register(Report)
admin.site.register(ContactMessage)