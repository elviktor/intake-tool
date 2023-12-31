from django.urls import reverse
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('book_detail', args=[str(self.id)])

    def __str__(self):
        return self.title

class Plant(models.Model):
    birth_date = models.DateField(null=True, blank=True)
    converted = models.BooleanField()
    deleted = models.BooleanField()
    destroy_reason = models.CharField(max_length=250, null=True, blank=True)
    destroy_reason_id = models.IntegerField(null=True, blank=True)
    destroy_scheduled = models.BooleanField()
    destroy_scheduled_time = models.DateTimeField(null=True, blank=True)
    external_id = models.CharField(max_length=250, null=True, blank=True)
    harvest_scheduled = models.BooleanField()
    biotrack_id = models.CharField(max_length=250, null=True, blank=True)
    location = models.CharField(max_length=250, null=True, blank=True)
    mother = models.BooleanField()
    org_id = models.IntegerField(null=True, blank=True)
    parent_id = models.CharField(max_length=250, null=True, blank=True)
    room_id = models.IntegerField(null=True, blank=True)
    session_time = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    strain = models.CharField(max_length=250, null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('plant_detail', args=[str(self.biotrack_id)])
    
    def __str__(self):
        return self.biotrack_id