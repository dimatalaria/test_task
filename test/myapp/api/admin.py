from django.contrib import admin

from . import models

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'category', 'is_notified', 'due_date', 'created_at')
    list_filter = ('is_notified', 'category', 'due_date')
    search_fields = ('title', 'description', 'user__username', 'category__name')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    fieldsets = (
            ('Основная информация', {
                'fields': ('title', 'description', 'category', 'user')
            }),
            ('Дополнительно', {
                'classes': ('collapse',),
                'fields': ('due_date', 'is_notified')
            }),
        )

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Task, TaskAdmin)

