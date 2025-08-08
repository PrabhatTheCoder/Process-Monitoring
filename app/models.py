from django.db import models
import uuid


class Host(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)  # Hostname of the machine
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SystemSnapshot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name='system_snapshots')

    os = models.CharField(max_length=255)
    processor = models.CharField(max_length=255)
    cpu_cores = models.IntegerField()
    threads = models.IntegerField()

    total_ram = models.FloatField(help_text="Total RAM in MB")
    available_ram = models.FloatField(help_text="Available RAM in MB")
    used_ram = models.FloatField(help_text="Used RAM in MB")

    total_storage = models.FloatField(help_text="Total storage in GB")
    used_storage = models.FloatField(help_text="Used storage in GB")
    available_storage = models.FloatField(help_text="Available storage in GB")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SystemSnapshot @ {self.created_at} on {self.host.name}"


class Process(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name='processes')

    pid = models.IntegerField()
    parent_pid = models.IntegerField(null=True, blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,  # Avoid recursive deletion
        null=True,
        blank=True,
        related_name='children'
    )

    name = models.CharField(max_length=255)
    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()

    time = models.DateTimeField(auto_now=True)  # Updates every stream

    class Meta:
        unique_together = ('host', 'pid')  # Optional: ensures uniqueness per machine

    def __str__(self):
        return f"{self.name} (PID {self.pid}) on {self.host.name}"


class Snapshot(models.Model):
    """
    Optional model to store historical CPU/memory snapshots per process.
    Use this if you want to chart CPU usage over time.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name='snapshots')
    time = models.DateTimeField(auto_now_add=True)

    # State at snapshot time
    name = models.CharField(max_length=255)
    pid = models.IntegerField()
    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()

    def __str__(self):
        return f"Snapshot of PID {self.pid} at {self.time}"
