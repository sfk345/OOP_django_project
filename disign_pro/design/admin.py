from django.contrib import admin

from design.models import Order, Category, User

admin.site.register(Category)
admin.site.register(Order)
admin.site.register(User)

