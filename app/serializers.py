from rest_framework import serializers
from .models import SystemSnapshot, Host, Process

class SystemSnapshotSerializer(serializers.ModelSerializer):
    hostname = serializers.SerializerMethodField()
    
    class Meta:
        model = SystemSnapshot
        fields = ['id','hostname',"os", "processor", "cpu_cores", "threads", "total_ram", "available_ram", "used_ram", "total_storage", "used_storage", "available_storage", "created_at", "host"]
        
    def get_hostname(self, obj):
        return obj.host.name if obj.host else None
    
class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = ['id','name', 'created_at']
    
class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = ['host', 'pid', 'parent_pid', 'name', 'cpu_usage', 'memory_usage', 'time']

    