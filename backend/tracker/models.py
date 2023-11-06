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
