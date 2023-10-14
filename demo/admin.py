from django.contrib import admin
from demo.models import Manager, UserPreference, Pharmacy, Drug

# Register your models here.
admin.site.register(Manager)
admin.site.register(UserPreference)
admin.site.register(Pharmacy)
admin.site.register(Drug)
