from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from .models import Host, SystemSnapshot, Process
from .serializers import SystemSnapshotSerializer, HostSerializer
from django.shortcuts import render


class SystemSnapshotView(APIView):
    def get(self, request):
        host_id = request.query_params.get("host_id")  # e.g., /api/snapshots?host_id=xxxx

        queryset = SystemSnapshot.objects.select_related("host").order_by("-created_at")

        if host_id:
            queryset = queryset.filter(host_id=host_id)

        serializer = SystemSnapshotSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class AvailableHost(APIView):
    def get(self, request):
        queryset = Host.objects.order_by("-created_at")
        serializers = HostSerializer(queryset, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    


def index_view(request):
    return render(request, 'index.html')

def live_view(request, hostname):
    return render(request, 'live.html', {'hostname': hostname})

def snapshot_view(request):
    return render(request, 'snapshot.html')