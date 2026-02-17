"""
Core models for security and utility features
"""
from django.db import models
from django.contrib.auth.models import User


class AuditLog(models.Model):
    """Audit trail for security"""
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
        ('login', 'Login'),
        ('logout', 'Logout'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    content_type = models.CharField(max_length=255)
    object_id = models.IntegerField(null=True, blank=True)
    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"
