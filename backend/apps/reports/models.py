"""
Models for violence reports
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class ViolenceType(models.Model):
    """Types de violences"""
    VIOLENCE_CHOICES = [
        ('physical', 'Violences Physiques'),
        ('sexual', 'Violences Sexuelles'),
        ('psychological', 'Violences Psychologiques'),
        ('economic', 'Violences Économiques'),
        ('social', 'Violences Sociales'),
    ]
    
    name = models.CharField(max_length=100, choices=VIOLENCE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Violence Types"
    
    def __str__(self):
        return self.get_name_display()


class Report(models.Model):
    """Déclaration de violence"""
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('submitted', 'Soumise'),
        ('reviewed', 'Examinée'),
        ('resolved', 'Résolue'),
    ]
    
    GENDER_CHOICES = [
        ('female', 'Femme'),
        ('male', 'Homme'),
        ('other', 'Autre'),
    ]
    
    # Informations de la victime
    victim_name = models.CharField(max_length=255)
    victim_age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)])
    victim_gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    victim_phone = models.CharField(max_length=20, blank=True)
    victim_email = models.EmailField(blank=True)
    
    # Détails du rapport
    violence_type = models.ForeignKey(ViolenceType, on_delete=models.PROTECT)
    description = models.TextField()
    location = models.CharField(max_length=255)
    incident_date = models.DateTimeField()
    
    # Métadonnées
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='reports')
    
    # Confidentialité
    is_anonymous = models.BooleanField(default=False)
    is_confidential = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['violence_type']),
        ]
    
    def __str__(self):
        return f"Report #{self.id} - {self.victim_name}"


class Attachment(models.Model):
    """Pièces jointes pour les rapports"""
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='reports/%Y/%m/%d/')
    file_type = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.file.name}"