from django.urls import path
from .views import SystemSnapshotView, AvailableHost
from . import views

urlpatterns = [
    path('system-snapshot/', SystemSnapshotView.as_view(), name='system_snapshot'),
    path('available-host/', AvailableHost.as_view()),
    
    path('', views.index_view, name='index'),
    path('live/<str:hostname>/', views.live_view, name='live'),
    path('snapshot/', views.snapshot_view, name='snapshot'),
    
]
