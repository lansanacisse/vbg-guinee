"""
URL configuration for reports app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportViewSet, ViolenceTypeViewSet

router = DefaultRouter()
router.register(r'', ReportViewSet, basename='report')
router.register(r'types', ViolenceTypeViewSet, basename='violence-type')

urlpatterns = [
    path('', include(router.urls)),
]