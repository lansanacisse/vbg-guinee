"""
Serializers for statistics app
"""
from rest_framework import serializers
from .models import StatisticSnapshot


class StatisticSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatisticSnapshot
        fields = [
            'id', 'total_reports', 'submitted_reports', 'resolved_reports',
            'physical_violence_count', 'sexual_violence_count',
            'psychological_violence_count', 'economic_violence_count',
            'social_violence_count', 'female_victims_count', 'male_victims_count',
            'average_victim_age', 'created_at'
        ]
        read_only_fields = fields