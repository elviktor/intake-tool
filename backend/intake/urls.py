from django.urls import path
from . import views, apis

urlpatterns = [
    path('api/moves', apis.get_moves, name='move_api'),
    path('api/sequences', apis.get_sequences, name='sequence_api'),
    path('api/sequencerecords', apis.get_sequencerecords, name='sequencerecord_api'),
]
