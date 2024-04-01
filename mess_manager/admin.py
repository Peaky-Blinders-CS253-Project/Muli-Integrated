# mess_manager/admin.py
from django.contrib import admin
from .models import MessMenu, FoodItem, Manager
from .models import Manager
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group


@admin.register(MessMenu)
class MessMenuAdmin(admin.ModelAdmin):
    list_display = ('day', 'breakfast', 'lunch', 'dinner', 'price')

admin.site.register(FoodItem)

admin.site.register(Manager)



class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_members_count')

    def get_members_count(self, obj):
        return obj.student_groups.count()  # Update attribute name
    get_members_count.short_description = 'Members Count'

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)