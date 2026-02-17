"""
API Views for statistics
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q, Avg
from apps.reports.models import Report, ViolenceType
from .models import StatisticSnapshot
from .serializers import StatisticSnapshotSerializer


class StatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for statistics"""
    queryset = StatisticSnapshot.objects.all()
    serializer_class = StatisticSnapshotSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest statistics"""
        latest_stats = StatisticSnapshot.objects.latest('created_at')
        serializer = self.get_serializer(latest_stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_violence_type(self, request):
        """Get statistics by violence type"""
        stats = Report.objects.filter(status='submitted').values('violence_type__name').annotate(
            count=Count('id')
        )
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def by_gender(self, request):
        """Get statistics by victim gender"""
        stats = Report.objects.filter(status='submitted').values('victim_gender').annotate(
            count=Count('id')
        )
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def by_location(self, request):
        """Get statistics by location"""
        stats = Report.objects.filter(status='submitted').values('location').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        return Response(stats)
    
    @action(detail=False, methods=['post'])
    def generate_snapshot(self, request):
        """Generate a new statistics snapshot"""
        reports = Report.objects.filter(status='submitted')
        
        snapshot = StatisticSnapshot.objects.create(
            total_reports=Report.objects.count(),
            submitted_reports=reports.count(),
            resolved_reports=Report.objects.filter(status='resolved').count(),
            physical_violence_count=reports.filter(violence_type__name='physical').count(),
            sexual_violence_count=reports.filter(violence_type__name='sexual').count(),
            psychological_violence_count=reports.filter(violence_type__name='psychological').count(),
            economic_violence_count=reports.filter(violence_type__name='economic').count(),
            social_violence_count=reports.filter(violence_type__name='social').count(),
            female_victims_count=reports.filter(victim_gender='female').count(),
            male_victims_count=reports.filter(victim_gender='male').count(),
            average_victim_age=reports.aggregate(Avg('victim_age'))['victim_age__avg'] or 0,
        )
        
        serializer = self.get_serializer(snapshot)
        return Response(serializer.data, status=status.HTTP_201_CREATED)