from django.contrib import admin

# Register your models here.
from users.models import User, EmailVerifyRecord

admin.site.register(User)
admin.site.register(EmailVerifyRecord)

