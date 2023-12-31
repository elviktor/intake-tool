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
    birth_date = models.DateField()
    converted = models.BooleanField()
    deleted = models.BooleanField()
    destroy_reason = models.CharField(max_length=250)
    destroy_reason_id = models.IntegerField()
    destroy_scheduled = models.BooleanField()
    destroy_scheduled_time = models.DateTimeField()
    external_id = models.CharField(max_length=250)
    harvest_scheduled = models.BooleanField()
    id = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    mother = models.BooleanField()
    org_id = models.IntegerField()
    parent_id = models.CharField(max_length=250)
    room_id = models.IntegerField()
    session_time = models.IntegerField()
    state = models.CharField(max_length=250)
    strain = models.CharField(max_length=250)
    transaction_id = models.IntegerField()

    def __str__(self):
        return self.id