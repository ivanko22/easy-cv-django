from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Social, Employment, CV

PREDEFINED_SOCIALS = [
    {"name": "+ Cell", "link": "+ Cell"},
    {"name": "+ Portfolio", "link": "+ Portfolio"},
    {"name": "+ Linkedin", "link": "+ Linkedin"},
    {"name": "+ Location", "link": "+ Location"},
    {"name": "+ Github", "link": "+ Github"},
    {"name": "+ Other", "link": "+ Other"},
]

@receiver(post_save, sender=User)
def create_default_socials(sender, instance, created, **kwargs):
    if created:  # Only when a user is created
        for social in PREDEFINED_SOCIALS:
            Social.objects.create(user=instance, name=social["name"], link=social["link"])

@receiver(post_save, sender=Employment)
def update_work_history_on_save(sender, instance, **kwargs):
    """
    Update the work_history for the user's single CV whenever an Employment record is saved.
    """
    user = instance.user
    employment_records = Employment.objects.filter(user=user)

    # Fetch the user's CV (since there's only one CV per user)
    cv = CV.objects.filter(user=user).first()
    if cv:
        cv.work_history.set(employment_records)  # Update work history

@receiver(post_delete, sender=Employment)
def update_work_history_on_delete(sender, instance, **kwargs):
    """
    Update the work_history for the user's single CV whenever an Employment record is deleted.
    """
    user = instance.user
    employment_records = Employment.objects.filter(user=user)

    # Fetch the user's CV (since there's only one CV per user)
    cv = CV.objects.filter(user=user).first()
    if cv:
        cv.work_history.set(employment_records)  # Update work history
        
