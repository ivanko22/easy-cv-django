from django.contrib import admin
from .models import Employment
@admin.register(Employment)
class EmploymentAdmin(admin.ModelAdmin):
    list_display = ('position', 'employer', 'startDate', 'endDate', 'description')