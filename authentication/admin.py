from django.contrib import admin

from authentication.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(UserToken)
admin.site.register(Reset)
admin.site.register(ActivationCode)
