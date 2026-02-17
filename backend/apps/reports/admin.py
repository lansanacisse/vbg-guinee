"""
Admin configuration for reports app
"""
from django.contrib import admin
from .models import Report, ViolenceType, Attachment


@admin.register(ViolenceType)
class ViolenceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['victim_name', 'violence_type', 'status', 'incident_date', 'created_at']
    list_filter = ['status', 'violence_type', 'created_at']
    search_fields = ['victim_name', 'victim_email', 'victim_phone']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [AttachmentInline]
    
    fieldsets = (
        ('Informations de la victime', {
            'fields': ('victim_name', 'victim_age', 'victim_gender', 'victim_phone', 'victim_email')
        }),
        ('Détails du rapport', {
            'fields': ('violence_type', 'description', 'location', 'incident_date')
        }),
        ('Statut et métadonnées', {
            'fields': ('status', 'is_anonymous', 'is_confidential', 'created_by', 'created_at', 'updated_at')
        }),
    )


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['file', 'report', 'file_type', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at']
    search_fields = ['file']