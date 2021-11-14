import uuid
from django.db import models
from django.utils import timezone
from accounts.models import CustomUser

class Issue(models.Model):
    """Model representing a client issue."""
    issue = models.CharField(max_length=200)

    def __str__(self):
        """String for representing the Model object."""
        return self.issue

class Keyword(models.Model):
    """Model representing a client issue."""
    keyword = models.CharField(max_length=200)

    def __str__(self):
        """String for representing the Model object."""
        return self.keyword

class Entity(models.Model):
    """Model representing a staff member."""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    longitude = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    url = models.URLField(max_length=200, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    social_media = models.CharField(max_length=200)
    comment = models.TextField(blank=True)


    class Meta:
        ordering = ['name']

    #def get_absolute_url(self):
    #    """Returns the url to access a particular author instance."""
    #    return reverse('staff_detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Rating(models.Model):
    """Model representing a client intake ticket."""
    entity = models.ForeignKey(Entity, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(null=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.entity


class Move(models.Model):
    """Model representing dialogue moves"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    TYPE = (
        ('g', 'Greeting'),
        ('t', 'Triage'),
        ('i', 'Issue'),
        ('q', 'Question'),
        ('r', 'Response'),
        ('c', 'Conclusion'),
    )

    type = models.CharField(
        max_length=1,
        choices=TYPE,
        default='q',
    )

    title = models.CharField(max_length=200)
    quote = models.CharField(max_length=500)

    # Emergency choice
    EMERGENCY = (
        ('y', 'Yes'),
        ('n', 'No'),
        ('u', 'Unknown'),
    )

    emergency = models.CharField(
        max_length=1,
        choices=EMERGENCY,
        default='n',
    )

    # Cross referencing fields
    entity = models.ManyToManyField(Entity, blank=True)
    issue = models.ManyToManyField(Issue, blank=True)
    keyword = models.ManyToManyField(Keyword, blank=True)

    # Additional fields
    link = models.URLField(blank=True)
    information = models.TextField(blank=True)


    def __str__(self):
        """String for representing the Model object."""

        return f'{self.type}_{self.title.lower().replace(" ", "_")}'


class Script(models.Model):
    """Model representing a script that organizes moves."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    date = models.DateField(default=timezone.now)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True)

    # Cross referencing fields
    entity = models.ManyToManyField(Entity, blank=True)
    issue = models.ManyToManyField(Issue, blank=True)
    keyword = models.ManyToManyField(Keyword, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.title.lower().replace(" ", "_")

class Sequence(models.Model):
    """Model representing a script sequence."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #title = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True)
    script = models.ForeignKey(Script, on_delete=models.SET_NULL, null=True)
    order_num = models.IntegerField(null=True)
    move = models.ForeignKey(Move, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.script}__{self.order_num}'

class SequenceRecord(models.Model):
    """Model that records the sequence that a user follows in intake tool"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    m1 = models.CharField(max_length=200)
    m2 = models.CharField(max_length=200, blank=True)
    m3 = models.CharField(max_length=200, blank=True)
    m4 = models.CharField(max_length=200, blank=True)
    m5 = models.CharField(max_length=200, blank=True)
    m6 = models.CharField(max_length=200, blank=True)
    m7 = models.CharField(max_length=200, blank=True)
    m8 = models.CharField(max_length=200, blank=True)
    m9 = models.CharField(max_length=200, blank=True)
    m10 = models.CharField(max_length=200, blank=True)
    m11 = models.CharField(max_length=200, blank=True)
    m12 = models.CharField(max_length=200, blank=True)
    m13 = models.CharField(max_length=200, blank=True)
    m14 = models.CharField(max_length=200, blank=True)
    m15 = models.CharField(max_length=200, blank=True)
    m16 = models.CharField(max_length=200, blank=True)
    m17 = models.CharField(max_length=200, blank=True)
    m18 = models.CharField(max_length=200, blank=True)
    m19 = models.CharField(max_length=200, blank=True)
    m20 = models.CharField(max_length=200, blank=True)
