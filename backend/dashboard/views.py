
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from projects.models import Project
from tasks.models import Task


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get projects accessible to the current user
        if user.is_superuser or user.role == User.Role.ADMIN:
            projects = Project.objects.all()
        else:
            projects = Project.objects.filter(
                Q(manager=user) | Q(members=user)
            ).distinct()

        # Get tasks belonging to accessible projects
        tasks = Task.objects.filter(project__in=projects)

        # Project statistics
        total_projects = projects.count()
        active_projects = projects.filter(
            status=Project.Status.ACTIVE
        ).count()
        completed_projects = projects.filter(
            status=Project.Status.COMPLETED
        ).count()

        # Task statistics
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(
            status=Task.Status.COMPLETED
        ).count()
        pending_tasks = tasks.filter(
            status=Task.Status.PENDING
        ).count()
        in_progress_tasks = tasks.filter(
            status=Task.Status.IN_PROGRESS
        ).count()
        blocked_tasks = tasks.filter(
            status=Task.Status.BLOCKED
        ).count()

        # Calculate completion percentage
        completion_rate = (
            round((completed_tasks / total_tasks) * 100, 2)
            if total_tasks > 0 else 0
        )

        # Get today's date and the next 7 days
        today = timezone.localdate()
        next_seven_days = today + timedelta(days=7)

        # Find overdue tasks
        overdue_tasks = tasks.filter(
            due_date__lt=today
        ).exclude(
            status=Task.Status.COMPLETED
        ).values(
            'id',
            'title',
            'due_date',
            'priority',
            'status',
            'project__name'
        )

        # Find upcoming tasks
        upcoming_tasks = tasks.filter(
            due_date__gte=today,
            due_date__lte=next_seven_days
        ).exclude(
            status=Task.Status.COMPLETED
        ).values(
            'id',
            'title',
            'due_date',
            'priority',
            'status',
            'project__name'
        )

        return Response({
            "projects": {
                "total": total_projects,
                "active": active_projects,
                "completed": completed_projects,
            },
            "tasks": {
                "total": total_tasks,
                "completed": completed_tasks,
                "pending": pending_tasks,
                "in_progress": in_progress_tasks,
                "blocked": blocked_tasks,
            },
            "completion_rate": completion_rate,

            "deadlines": {
                "overdue_count": overdue_tasks.count(),
                "upcoming_count": upcoming_tasks.count(),
                "overdue_tasks": list(overdue_tasks),
                "upcoming_tasks": list(upcoming_tasks),
            },
        })



from django.shortcuts import get_object_or_404


class ProjectProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        user = request.user

        # Check which projects the user can access
        if user.is_superuser or user.role == User.Role.ADMIN:
            projects = Project.objects.all()
        else:
            projects = Project.objects.filter(
                Q(manager=user) | Q(members=user)
            ).distinct()

        project = get_object_or_404(projects, id=project_id)

        # Get tasks and milestones for this project
        tasks = Task.objects.filter(project=project)
        milestones = project.milestones.all()

        # Task statistics
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(
            status=Task.Status.COMPLETED
        ).count()
        pending_tasks = tasks.filter(
            status=Task.Status.PENDING
        ).count()
        in_progress_tasks = tasks.filter(
            status=Task.Status.IN_PROGRESS
        ).count()
        blocked_tasks = tasks.filter(
            status=Task.Status.BLOCKED
        ).count()

        task_progress = (
            round((completed_tasks / total_tasks) * 100, 2)
            if total_tasks else 0
        )

        # Milestone statistics
        total_milestones = milestones.count()
        completed_milestones = milestones.filter(
            status='COMPLETED'
        ).count()

        milestone_progress = (
            round((completed_milestones / total_milestones) * 100, 2)
            if total_milestones else 0
        )

        return Response({
            "project": {
                "id": project.id,
                "name": project.name,
                "status": project.status,
                "start_date": project.start_date,
                "end_date": project.end_date,
            },
            "tasks": {
                "total": total_tasks,
                "completed": completed_tasks,
                "pending": pending_tasks,
                "in_progress": in_progress_tasks,
                "blocked": blocked_tasks,
                "completion_rate": task_progress,
            },
            "milestones": {
                "total": total_milestones,
                "completed": completed_milestones,
                "completion_rate": milestone_progress,
            },
        })



class WorkloadAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Determine which tasks the user can analyze
        if user.is_superuser or user.role == User.Role.ADMIN:
            tasks = Task.objects.all()
            assigned_users = User.objects.filter(
                assigned_tasks__isnull=False
            ).distinct()

        elif user.role == User.Role.PROJECT_MANAGER:
            projects = Project.objects.filter(manager=user)
            tasks = Task.objects.filter(project__in=projects)
            assigned_users = User.objects.filter(
                assigned_tasks__project__in=projects
            ).distinct()

        else:
            tasks = Task.objects.filter(assigned_to=user)
            assigned_users = User.objects.filter(id=user.id)

        workload_data = []

        for member in assigned_users:
            member_tasks = tasks.filter(assigned_to=member)

            total = member_tasks.count()
            completed = member_tasks.filter(
                status=Task.Status.COMPLETED
            ).count()
            pending = member_tasks.filter(
                status=Task.Status.PENDING
            ).count()
            in_progress = member_tasks.filter(
                status=Task.Status.IN_PROGRESS
            ).count()
            blocked = member_tasks.filter(
                status=Task.Status.BLOCKED
            ).count()

            active = total - completed

            if active > 5:
                workload_level = "HIGH"
            elif active >= 3:
                workload_level = "MEDIUM"
            else:
                workload_level = "NORMAL"

            workload_data.append({
                "user_id": member.id,
                "username": member.username,
                "role": member.role,
                "total_tasks": total,
                "completed_tasks": completed,
                "pending_tasks": pending,
                "in_progress_tasks": in_progress,
                "blocked_tasks": blocked,
                "active_tasks": active,
                "workload_level": workload_level,
            })

        return Response({
            "total_members": len(workload_data),
            "workload": workload_data,
        })
