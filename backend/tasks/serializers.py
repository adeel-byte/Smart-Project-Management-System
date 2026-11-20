from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):

    assigned_to_name = serializers.CharField(
        source='assigned_to.username',
        read_only=True
    )

    created_by_name = serializers.CharField(
        source='created_by.username',
        read_only=True
    )

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = (
            'created_by',
            'created_at',
            'updated_at',
        )

    def validate(self, data):
        project = data.get(
            'project',
            getattr(self.instance, 'project', None)
        )

        start_date = data.get(
            'start_date',
            getattr(self.instance, 'start_date', None)
        )

        due_date = data.get(
            'due_date',
            getattr(self.instance, 'due_date', None)
        )

        if start_date and due_date and due_date < start_date:
            raise serializers.ValidationError(
                "Task due date cannot be earlier than its start date."
            )

        if project and start_date and due_date:
            if start_date < project.start_date or due_date > project.end_date:
                raise serializers.ValidationError(
                    "Task dates must be within the project schedule."
                )

        assigned_to = data.get(
            'assigned_to',
            getattr(self.instance, 'assigned_to', None)
        )

        if assigned_to and project:
            is_project_member = project.members.filter(
                id=assigned_to.id
            ).exists()

            is_project_manager = project.manager_id == assigned_to.id

            if not (is_project_member or is_project_manager):
                raise serializers.ValidationError({
                    'assigned_to': 'This user is not a member or manager of this project.'
                })

        return data