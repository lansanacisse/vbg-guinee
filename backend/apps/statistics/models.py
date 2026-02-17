"""
Models for statistics
"""
from django.db import models
from django.utils import timezone


class StatisticSnapshot(models.Model):
    """Snapshot des statistiques"""
    total_reports = models.IntegerField(default=0)
    submitted_reports = models.IntegerField(default=0)
    resolved_reports = models.IntegerField(default=0)
    
    # Par type de violence
    physical_violence_count = models.IntegerField(default=0)
    sexual_violence_count = models.IntegerField(default=0)
    psychological_violence_count = models.IntegerField(default=0)
    economic_violence_count = models.IntegerField(default=0)
    social_violence_count = models.IntegerField(default=0)
    
    # Démographique
    female_victims_count = models.IntegerField(default=0)
    male_victims_count = models.IntegerField(default=0)
    average_victim_age = models.FloatField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Statistics Snapshot - {self.created_at}"