import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.utils.timezone import now
from datetime import timedelta

from app.models import Host, Process, SystemSnapshot
from app.serializers import ProcessSerializer, SystemSnapshotSerializer
from channels.layers import get_channel_layer
from collections import defaultdict

class ProcessBroadcastConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.hostname = self.scope['url_route']['kwargs']['hostname']
        self.group_name = f"host_{self.hostname}"

        # Join group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print(f"Client subscribed to real-time process data of: {self.hostname}")

        # Send initial data when client connects
        await self.send_initial_data()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f"Client unsubscribed: {self.hostname}")

    async def receive(self, text_data):
        """Handle client messages like refresh requests"""
        try:
            data = json.loads(text_data)
            if data.get('action') == 'refresh':
                await self.send_initial_data()
        except:
            pass

    async def send_initial_data(self):
        """Send current process hierarchy to newly connected client"""
        try:
            processes = await self.get_process_hierarchy()
            await self.send(text_data=json.dumps({
                "host": self.hostname,
                "timestamp": str(now()),
                "processes": processes,
            }))
        except Exception as e:
            print(f"Error sending initial data: {e}")

    async def send_process_data(self, event):
        # Send data to client
        await self.send(text_data=json.dumps(event['data']))

    @sync_to_async
    def get_process_hierarchy(self):
        """Build process tree hierarchy"""
        try:
            host = Host.objects.get(name=self.hostname)
            processes = list(Process.objects.filter(host=host).select_related('parent'))
            
            # Build hierarchy
            process_map = {p.pid: p for p in processes}
            root_processes = []
            
            def serialize_process_with_children(process):
                children = [serialize_process_with_children(child) 
                           for child in processes if child.parent_pid == process.pid]
                
                return {
                    'pid': process.pid,
                    'parent_pid': process.parent_pid,
                    'name': process.name,
                    'cpu_usage': process.cpu_usage,
                    'memory_usage': process.memory_usage,
                    'children': children
                }
            
            # Find root processes (no parent or parent not in current dataset)
            for process in processes:
                if not process.parent_pid or process.parent_pid not in process_map:
                    root_processes.append(serialize_process_with_children(process))
            
            return root_processes
        except Exception as e:
            print(f"Error building hierarchy: {e}")
            return []


class ProcessStreamConsumer(AsyncWebsocketConsumer):
    last_snapshot_time = defaultdict(lambda: None)

    async def connect(self):
        await self.accept()
        print("WebSocket connection accepted")

    async def disconnect(self, close_code):
        print("WebSocket disconnected")
        
    async def broadcast_to_clients(self, hostname, timestamp, processes):
        """Broadcast process hierarchy to all connected clients"""
        channel_layer = get_channel_layer()
        group_name = f"host_{hostname}"

        # Build hierarchy for broadcasting
        process_hierarchy = await self.build_process_hierarchy(processes)

        await channel_layer.group_send(
            group_name,
            {
                "type": "send_process_data",
                "data": {
                    "host": hostname,
                    "timestamp": str(timestamp),
                    "processes": process_hierarchy,
                }
            }
        )

    @sync_to_async
    def build_process_hierarchy(self, processes):
        """Build hierarchical structure from flat process list"""
        # Create process map
        process_map = {}
        for proc in processes:
            process_map[proc['pid']] = {**proc, 'children': []}
        
        # Build parent-child relationships
        root_processes = []
        for proc in processes:
            parent_pid = proc.get('parent_pid')
            if not parent_pid or parent_pid not in process_map:
                # Root process
                root_processes.append(process_map[proc['pid']])
            else:
                # Add as child to parent
                process_map[parent_pid]['children'].append(process_map[proc['pid']])
        
        return root_processes

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            system_info = data.get("system_info")
            processes = data.get("processes")

            if not system_info or not processes:
                await self.send(text_data=json.dumps({"error": "Missing system_info or processes"}))
                return

            # Handle or create Host
            hostname = system_info["hostname"]
            host, _ = await sync_to_async(Host.objects.get_or_create)(name=hostname)
            
            # Current timestamp
            timestamp = now()

            # Save system snapshot (every 60 seconds per host)
            await self.save_system_snapshot(host, system_info)
            
            # Save process list WITH HIERARCHY
            await self.save_processes(host, processes)

            # Broadcast to clients AFTER saving (so hierarchy is built)
            await self.broadcast_to_clients(hostname, timestamp, processes)

        except Exception as e:
            print("Error handling WebSocket message:", e)
            await self.send(text_data=json.dumps({"error": str(e)}))

    @sync_to_async
    def save_system_snapshot(self, host, system_info):
        now_time = now()
        last_time = self.last_snapshot_time.get(host.id)

        if last_time and (now_time - last_time) < timedelta(seconds=60):
            print(f"[{host.name}] Skipping snapshot (taken recently)")
            return

        self.last_snapshot_time[host.id] = now_time

        snapshot_data = {
            **system_info,
            "host": host.id,
            "time": now_time,
        }

        serializer = SystemSnapshotSerializer(data=snapshot_data)
        if serializer.is_valid():
            serializer.save()
            print(f"[{host.name}] Snapshot saved at {now_time}")
        else:
            print("Snapshot validation error:", serializer.errors)

    @sync_to_async
    def save_processes(self, host, processes):
        """Save processes with proper parent-child relationships"""
        now_time = now()

        # Clear previous processes
        Process.objects.filter(host=host).delete()

        # First pass: Create all processes without parent relationships
        process_objects = {}
        for proc in processes:
            try:
                process_obj = Process.objects.create(
                    host=host,
                    pid=proc["pid"],
                    parent_pid=proc.get("parent_pid"),
                    name=proc["name"],
                    cpu_usage=proc["cpu_usage"],
                    memory_usage=proc["memory_usage"],
                    time=now_time,
                    parent=None  # Set this in second pass
                )
                process_objects[proc["pid"]] = process_obj
                print(f"Created process: {proc['name']} (PID: {proc['pid']}, Parent: {proc.get('parent_pid', 'None')})")
            except Exception as e:
                print(f"Error creating process {proc.get('pid')}: {e}")

        # Second pass: Set parent relationships using the `parent` field
        for proc in processes:
            parent_pid = proc.get("parent_pid")
            if parent_pid and parent_pid in process_objects:
                try:
                    child_process = process_objects[proc["pid"]]
                    parent_process = process_objects[parent_pid]
                    child_process.parent = parent_process
                    child_process.save()
                    print(f"Linked {child_process.name} -> {parent_process.name}")
                except Exception as e:
                    print(f"Error linking parent-child: {e}")

        print(f"[{host.name}] Saved {len(process_objects)} processes with hierarchy")