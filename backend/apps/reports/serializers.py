"""
Serializers for reports app
"""
from rest_framework import serializers
from .models import Report, ViolenceType, Attachment


class ViolenceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViolenceType
        fields = ['id', 'name', 'description']


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'file', 'file_type', 'uploaded_at']
        read_only_fields = ['uploaded_at']


class ReportSerializer(serializers.ModelSerializer):
    violence_type_name = serializers.CharField(source='violence_type.get_name_display', read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Report
        fields = [
            'id', 'victim_name', 'victim_age', 'victim_gender', 'victim_phone', 'victim_email',
            'violence_type', 'violence_type_name', 'description', 'location', 'incident_date',
            'status', 'is_anonymous', 'is_confidential', 'created_by_username', 'created_at', 'updated_at',
            'attachments'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by_username']
