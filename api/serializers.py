from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import CV, Employment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class EmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employment
        fields = ['id', 'position', 'employer', 'startDate', 'endDate', 'description']
        read_only_fields = ['user'] 

    def create(self, validated_data):
        return Employment.objects.create(**validated_data)
    
class CVSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = CV
        fields = [
            'id', 'user', 'profile_image', 'phone_number', 'job_title', 
            'job_category', 'overview', 'experience', 'skills', 
            'languages', 'work_history',
        ]
