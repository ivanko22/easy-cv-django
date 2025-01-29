from django.contrib import admin
from .models import Employment, CV, Social
@admin.register(Employment)
class EmploymentAdmin(admin.ModelAdmin):
    list_display = ('position', 'employer', 'startDate', 'endDate', 'description')
from django.contrib import admin
from .models import CV, Employment

@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = [
        'user', 
        'job_title', 
        'job_category', 
        'skills',
        'languages',
        'experience', 
        'phone_number', 
        'get_work_history',  # Custom method to display work history
    ]

    def get_work_history(self, obj):
        # Check if the object has work history and join positions with employers
        if obj.work_history.exists():
            return ", ".join([f"{job.position} at {job.employer}" for job in obj.work_history.all()])
        return "No work history"

    # Add a human-readable label for the column
    get_work_history.short_description = "Work History"

    # Enable horizontal filtering for ManyToMany relationships in admin forms
    filter_horizontal = ('work_history',)

@admin.register(Social)
class SocialAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "link")
    search_fields = ("user__username", "name", "link")
    list_filter = ("name",)
