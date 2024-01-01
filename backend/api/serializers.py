from rest_framework import serializers
from tracker.models import Book, Plant

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'subtitle', 'author', 'isbn')

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ('biotrack_id', 'strain', 'birth_date', 'location')