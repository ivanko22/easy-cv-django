from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import CV, Employment

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Serializer for the Employment model
class EmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employment
        fields = '__all__'

# Serializer for the CV model
class CVSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = CV
        fields = [
            'id', 'user', 'profile_image', 'phone_number', 'job_title', 
            'job_category', 'overview', 'experience', 'skills', 
            'languages', 'work_history',
        ]
