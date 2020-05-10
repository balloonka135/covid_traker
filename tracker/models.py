from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    profile_url = models.URLField(blank=True)
    occupation = models.CharField(
        verbose_name=_('Occupation type'),
        help_text="Enter your occupation (e.g. student)",
        max_length=100,
        blank=True
    )
    infection_status = models.CharField(
        verbose_name=_('Infection status'),
        help_text="Enter your infection status (e.g. treated)",
        max_length=100,
        blank=True
    )

    def __str__(self):
        return self.user.username
