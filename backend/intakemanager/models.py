import uuid
from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
from intake.models import Area, Issue, Keyword


class MSCGroup(models.Model):
    """Model for geographic regions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_name = models.CharField(max_length=200)
    issue = models.ManyToManyField(Issue, blank=True)
    keyword = models.ManyToManyField(Keyword, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.group_name

class IntakeUser(models.Model):
    """Model representing a staff member."""
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    area = models.ManyToManyField(Area, blank=True)
    msc_group = models.ManyToManyField(MSCGroup, blank=True)

    STATUS = (
        ('a', 'active'),
        ('i', 'inactive'),
        ('h', 'hiatus'),
        ('u', 'unknown'),
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        default='u',
    )

    start_date = models.DateField(default=timezone.now, null=True)
    end_date = models.DateField(blank=True, null=True)
    schedule = models.URLField(blank=True)
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
