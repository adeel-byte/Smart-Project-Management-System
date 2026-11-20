
from django.urls import path
from .views import (
    DashboardView,
    ProjectProgressView,
    WorkloadAnalysisView,
)

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path(
        'dashboard/projects/<int:project_id>/',
        ProjectProgressView.as_view(),
        name='project-progress'
    ),

    path(
        'dashboard/workload/',
        WorkloadAnalysisView.as_view(),
        name='workload-analysis'
    ),
]
