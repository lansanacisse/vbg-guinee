"""
Admin configuration for statistics app
"""
from django.contrib import admin
from .models import StatisticSnapshot


@admin.register(StatisticSnapshot)
class StatisticSnapshotAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'total_reports', 'submitted_reports', 'resolved_reports']
    readonly_fields = ['total_reports', 'submitted_reports', 'resolved_reports',
        'physical_violence_count', 'sexual_violence_count',
        'psychological_violence_count', 'economic_violence_count',
        'social_violence_count', 'female_victims_count', 'male_victims_count',
        'average_victim_age', 'created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
