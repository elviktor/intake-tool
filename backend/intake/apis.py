from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Move, Sequence
from .serializers import MoveSerializer, SequenceSerializer

import requests
import json

@login_required
def get_moves(request):
    moves = MoveSerializer(
        Move.objects.all().order_by("title"),
        many = True
    ).data

    return JsonResponse({"moves": moves})

@login_required
def get_sequences(request):
    sequences = SequenceSerializer(
        Sequence.objects.all(),
        many = True
    ).data

    return JsonResponse({"sequences": sequences})
