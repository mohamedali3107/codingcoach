from rest_framework import serializers
from .models import TeamMood

class MoodSerializer(serializers.Serializer):
    moodLevel = serializers.IntegerField()
    message = serializers.CharField(allow_blank=True)
    projectName = serializers.CharField(allow_blank=True)

