from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import CV, Employment, Social

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
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    work_history = EmploymentSerializer(many=True, required=False)
    class Meta:
        model = CV
        fields = [
            'id', 'user', 'first_name', 'last_name', 'profile_image', 'phone_number', 'job_title', 
            'job_category', 'overview', 'experience', 'skills', 
            'languages', 'work_history',
        ]

    def create(self, validated_data):
        user = self.context['request'].user

        # Delete any existing CV for the user
        CV.objects.filter(user=user).delete()

        # Create a new CV
        cv = CV.objects.create(user=user, **validated_data)

        # Automatically fetch ALL existing Employment records for the user
        existing_employments = Employment.objects.filter(user=user)

        # Associate all employment records with the new CV
        cv.work_history.set(existing_employments)

        return cv
    
    def update(self, instance, validated_data):
        # Extract and remove the work_history data from validated_data
        work_history_data = validated_data.pop('work_history', None)
        print("Work History Data (Update):", work_history_data)  # Debug print

        # Update other fields of the CV
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update work_history if provided
        if work_history_data:
            instance.work_history.clear()  # Clear existing relationships
            for employment_data in work_history_data:
                employment = Employment.objects.create(**employment_data, user=instance.user)
                instance.work_history.add(employment)

        return instance

class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = ['id', 'name', 'link', 'user']
        read_only_fields = ['user']  # Make 'user' read-only
