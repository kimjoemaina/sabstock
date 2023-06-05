from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib.auth.models import Permission
def permission_string_method(self:Permission):
    return f'{self.codename}'
Permission.__str__ = permission_string_method

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(Input)
admin.site.register(Output)
admin.site.register(ConstructionSite)
admin.site.register(ConstructionPermission)
