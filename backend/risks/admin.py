
from django.contrib import admin
from .models import Risk


@admin.register(Risk)
class RiskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'project',
        'category',
        'probability',
        'impact',
        'status',
        'identified_by'
    )

    list_filter = ('category', 'status')

    search_fields = ('title', 'description', 'project__name')
