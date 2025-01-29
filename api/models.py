from django.db import models
from django.contrib.auth.models import User

class Employment(models.Model):
    position = models.CharField(max_length=255)
    employer = models.CharField(max_length=255)
    startDate = models.DateField()
    endDate = models.DateField(blank=True, null=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employments")
    
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

PREDEFINED_SOCIALS = [
    {"name": "+ Cell", "link": "+ Cell"},
    {"name": "+ Portfolio", "link": "+ Portfolio"},
    {"name": "+ Linkedin", "link": "+ Linkedin"},
    {"name": "+ Location", "link": "+ Location"},
    {"name": "+ Github", "link": "+ Github"},
    {"name": "+ Other", "link": "+ Other"},
]

class Social(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="socials")
    name = models.CharField(max_length=100, choices=[(social["name"], social["name"]) for social in PREDEFINED_SOCIALS])
    link = models.CharField(max_length=255, default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "name"], name="unique_user_social_name"),
        ]

    def __str__(self):
        return f"{self.name}: {self.link}"
