from django.db import models
from django.contrib.auth.models import User  # Using Django's default User model

class Employment(models.Model):
    """Model for employment history."""
    position = models.CharField(max_length=255)
    employer = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.position} at {self.employer}"

class CV(models.Model):
    """Model for CVs."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cvs")
    profile_image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    job_category = models.CharField(max_length=255, blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    experience = models.PositiveIntegerField()  
    skills = models.JSONField(blank=True, null=True)  
    languages = models.JSONField(blank=True, null=True)  
    work_history = models.ManyToManyField(Employment, blank=True, related_name="cvs")

    def __str__(self):
        return f"{self.user}'s CV - {self.job_title or 'Untitled'}"

class Language(models.Model):
    """Model for languages known by the user."""
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.level})"

class Social(models.Model):
    """Model for social links associated with the user."""
    name = models.CharField(max_length=100)
    link = models.URLField()

    def __str__(self):
        return f"{self.name}: {self.link}"
