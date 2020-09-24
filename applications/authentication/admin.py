from django.contrib import admin
from .models import User
# Register your models here.

class User_Admin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'email'
    )

    search_fields = ('first_name', 'last_name', 'username', 'email')
    #list_filter = ()

admin.site.register(User, User_Admin)