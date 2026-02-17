"""
API Views for reports
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Report, ViolenceType
from .serializers import ReportSerializer, ViolenceTypeSerializer


class ViolenceTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for violence types"""
    queryset = ViolenceType.objects.all()
    serializer_class = ViolenceTypeSerializer
    permission_classes = [IsAuthenticated]


class ReportViewSet(viewsets.ModelViewSet):
    """API endpoint for violence reports"""
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'violence_type', 'incident_date']
    search_fields = ['victim_name', 'victim_email', 'location']
    ordering_fields = ['created_at', 'incident_date']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def submit_report(self, request, pk=None):
        """Change report status to submitted"""
        report = self.get_object()
        report.status = 'submitted'
        report.save()
        return Response({'status': 'Report submitted'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def my_reports(self, request):
        """Get current user's reports"""
        reports = Report.objects.filter(created_by=request.user)
        serializer = self.get_serializer(reports, many=True)
        return Response(serializer.data)