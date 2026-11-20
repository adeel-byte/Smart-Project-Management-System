from django.urls import path
from .views import ProjectReportView, ProjectReportCSVView

urlpatterns = [
    path(
        'reports/project/<int:project_id>/',
        ProjectReportView.as_view(),
        name='project-report'
    ),
    path(
        'reports/project/<int:project_id>/csv/',
        ProjectReportCSVView.as_view(),
        name='project-report-csv'
    ),
]