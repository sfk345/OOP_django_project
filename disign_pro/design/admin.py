from django.contrib import admin

from design.models import *

admin.site.register(User)
admin.site.register(Application)
admin.site.register(Category)
admin.site.register(Order)

