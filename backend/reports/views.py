import csv
from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from projects.models import Project
from tasks.models import Task
from risks.models import Risk


class ProjectReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):

        # Get the requested project
        project = get_object_or_404(Project, id=project_id)

        # Check whether the user can access this project
        is_admin = request.user.is_superuser or request.user.role == 'ADMIN'

        if not is_admin:
            if (
                project.manager_id != request.user.id
                and not project.members.filter(id=request.user.id).exists()
            ):
                raise PermissionDenied(
                    "You do not have permission to view this project report."
                )

        # Fetch project tasks, milestones, and risks
        tasks = Task.objects.filter(project=project).select_related(
            'assigned_to', 'created_by'
        )

        milestones = project.milestones.all()

        risks = Risk.objects.filter(project=project)

        # Task statistics
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status='COMPLETED').count()
        pending_tasks = tasks.filter(status='PENDING').count()
        in_progress_tasks = tasks.filter(status='IN_PROGRESS').count()
        blocked_tasks = tasks.filter(status='BLOCKED').count()

        completion_rate = (
            round((completed_tasks / total_tasks) * 100, 2)
            if total_tasks else 0
        )

        # Prepare task details
        task_details = []

        for task in tasks:
            task_details.append({
                'id': task.id,
                'title': task.title,
                'assigned_to': (
                    task.assigned_to.username if task.assigned_to else None
                ),
                'created_by': task.created_by.username,
                'start_date': task.start_date,
                'due_date': task.due_date,
                'priority': task.priority,
                'status': task.status,
            })

        # Prepare milestone details
        milestone_details = []

        for milestone in milestones:
            milestone_details.append({
                'id': milestone.id,
                'title': milestone.title,
                'description': milestone.description,
                'due_date': milestone.due_date,
                'status': milestone.status,
            })

        # Prepare risk details
        risk_details = []

        for risk in risks:
            risk_details.append({
                'id': risk.id,
                'title': risk.title,
                'category': risk.category,
                'probability': risk.probability,
                'impact': risk.impact,
                'risk_exposure': risk.risk_exposure,
                'status': risk.status,
                'mitigation_plan': risk.mitigation_plan,
            })

        # Calculate workload for project members
        workload = []

        for member in project.members.all():
            member_tasks = tasks.filter(assigned_to=member)

            workload.append({
                'member': member.username,
                'total_tasks': member_tasks.count(),
                'completed_tasks': member_tasks.filter(
                    status='COMPLETED'
                ).count(),
                'active_tasks': member_tasks.exclude(
                    status='COMPLETED'
                ).count(),
            })

        # Final report
        report = {
            'project': {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'manager': project.manager.username,
                'start_date': project.start_date,
                'end_date': project.end_date,
                'status': project.status,
            },
            'task_summary': {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'pending_tasks': pending_tasks,
                'in_progress_tasks': in_progress_tasks,
                'blocked_tasks': blocked_tasks,
                'completion_rate': completion_rate,
            },
            'tasks': task_details,
            'milestones': milestone_details,
            'risks': risk_details,
            'team_workload': workload,
        }

        return Response(report)


class ProjectReportCSVView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):

        project = get_object_or_404(Project, id=project_id)

        # Check project access
        is_admin = (
            request.user.is_superuser
            or request.user.role == 'ADMIN'
        )

        if not is_admin:
            if (
                project.manager_id != request.user.id
                and not project.members.filter(id=request.user.id).exists()
            ):
                raise PermissionDenied(
                    "You do not have permission to download this report."
                )

        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = (
            f'attachment; filename="SPMS_Project_{project.id}_Report.csv"'
        )

        writer = csv.writer(response)

        writer.writerow([
            'Record Type',
            'ID',
            'Name / Title',
            'Category / Assigned To',
            'Start Date',
            'Due Date',
            'Status',
            'Priority',
            'Probability',
            'Impact',
            'Risk Exposure',
            'Details',
        ])

        # Project information
        writer.writerow([
            'PROJECT',
            project.id,
            project.name,
            project.manager.username,
            project.start_date,
            project.end_date,
            project.status,
            '',
            '',
            '',
            '',
            project.description,
        ])

        # Tasks
        tasks = Task.objects.filter(project=project).select_related(
            'assigned_to'
        )

        for task in tasks:
            writer.writerow([
                'TASK',
                task.id,
                task.title,
                task.assigned_to.username if task.assigned_to else 'Unassigned',
                task.start_date,
                task.due_date,
                task.status,
                task.priority,
                '',
                '',
                '',
                task.description,
            ])

        # Milestones
        for milestone in project.milestones.all():
            writer.writerow([
                'MILESTONE',
                milestone.id,
                milestone.title,
                '',
                '',
                milestone.due_date,
                milestone.status,
                '',
                '',
                '',
                '',
                milestone.description,
            ])

        # Risks
        for risk in Risk.objects.filter(project=project):
            writer.writerow([
                'RISK',
                risk.id,
                risk.title,
                risk.category,
                '',
                '',
                risk.status,
                '',
                risk.probability,
                risk.impact,
                risk.risk_exposure,
                risk.mitigation_plan,
            ])

        # Team workload
        for member in project.members.all():
            member_tasks = tasks.filter(assigned_to=member)

            writer.writerow([
                'TEAM WORKLOAD',
                member.id,
                member.username,
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                (
                    f"Total Tasks: {member_tasks.count()}, "
                    f"Completed: {member_tasks.filter(status='COMPLETED').count()}, "
                    f"Active: {member_tasks.exclude(status='COMPLETED').count()}"
                ),
            ])

        return response