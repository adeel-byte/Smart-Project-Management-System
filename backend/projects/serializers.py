from rest_framework import serializers
from .models import Project, Milestone
from accounts.models import User


class ProjectSerializer(serializers.ModelSerializer):

    manager_name = serializers.CharField(
        source='manager.username',
        read_only=True
    )

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('manager', 'created_at', 'updated_at')

    def validate_members(self, members):
        for member in members:
            if member.role != User.Role.TEAM_MEMBER:
                raise serializers.ValidationError(
                    f"{member.username} is not a Team Member."
                )
        return members

    def validate(self, data):
        start_date = data.get(
            'start_date',
            getattr(self.instance, 'start_date', None)
        )
        end_date = data.get(
            'end_date',
            getattr(self.instance, 'end_date', None)
        )

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError(
                "End date cannot be earlier than start date."
            )

        return data


class MilestoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Milestone
        fields = '__all__'
        read_only_fields = ('created_at',)

    def validate(self, data):
        project = data.get(
            'project',
            getattr(self.instance, 'project', None)
        )
        due_date = data.get(
            'due_date',
            getattr(self.instance, 'due_date', None)
        )

        if project and due_date:
            if due_date < project.start_date or due_date > project.end_date:
                raise serializers.ValidationError(
                    "Milestone due date must be within the project dates."
                )

        return data