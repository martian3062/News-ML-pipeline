"""
User model with AI personalization fields.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended user with AI personalization fields."""

    PROFILE_TYPES = [
        ("investor", "Investor"),
        ("founder", "Startup Founder"),
        ("student", "Student"),
        ("professional", "Working Professional"),
        ("executive", "Corporate Executive"),
        ("other", "Other"),
    ]

    profile_type = models.CharField(max_length=20, choices=PROFILE_TYPES, default="other")
    preferred_language = models.CharField(max_length=5, default="en")
    interests = models.JSONField(default=list, blank=True)
    financial_goals = models.JSONField(default=list, blank=True)
    onboarding_completed = models.BooleanField(default=False)
    concierge_profile = models.JSONField(default=dict, blank=True)
    avatar_url = models.URLField(max_length=500, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username
