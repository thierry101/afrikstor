from django.contrib import admin

from settingSite.models import ConfidentialityAndRule, SettingSite

# Register your models here.


admin.site.register(SettingSite)
admin.site.register(ConfidentialityAndRule)
