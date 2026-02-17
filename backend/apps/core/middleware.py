"""
Middleware for security features
"""
import json
from .models import AuditLog


class AuditLoggingMiddleware:
    """Middleware to log user actions"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Log user actions
        if request.user.is_authenticated:
            # Determine action based on method
            action = 'view'
            if request.method == 'POST':
                action = 'create'
            elif request.method == 'PUT' or request.method == 'PATCH':
                action = 'update'
            elif request.method == 'DELETE':
                action = 'delete'
            
            # Extract IP address
            ip_address = self.get_client_ip(request)
            
            AuditLog.objects.create(
                user=request.user,
                action=action,
                content_type=request.path,
                ip_address=ip_address,
            )
        
        return response
    
    @staticmethod
    def get_client_ip(request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
