
from rest_framework import serializers
from .models import Risk


class RiskSerializer(serializers.ModelSerializer):
    identified_by_name = serializers.CharField(
        source='identified_by.username',
        read_only=True
    )

    risk_exposure = serializers.ReadOnlyField()

    class Meta:
        model = Risk
        fields = '__all__'
        read_only_fields = (
            'identified_by',
            'created_at',
            'updated_at',
        )

    def validate_probability(self, value):
        if value < 0 or value > 1:
            raise serializers.ValidationError(
                "Probability must be between 0.00 and 1.00."
            )
        return value

    def validate_impact(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Impact must be between 1 and 5."
            )
        return value
