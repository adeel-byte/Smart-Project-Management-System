from django.contrib import admin
from .models import Project, Milestone


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'manager',
        'start_date',
        'end_date',
        'status',
    )

    list_filter = ('status', 'start_date')

    search_fields = ('name', 'description', 'manager__username')

    filter_horizontal = ('members',)


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'project',
        'due_date',
        'status',
    )

    list_filter = ('status', 'due_date')

    search_fields = ('title', 'project__name')