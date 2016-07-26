from django.contrib import admin
from models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'team', 'reports_to')

admin.site.register(Account, AccountAdmin)
