from django.contrib import admin
# Register your models here.
from authentication.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


admin.site.register(ContentType)
admin.site.register(Permission)

admin.site.register(User)
