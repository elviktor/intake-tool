from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Move, Sequence
from .serializers import MoveSerializer, SequenceSerializer

import requests
import json

@api_view(['GET', 'POST'])
@csrf_exempt
def get_moves(request):
    if request.method == 'POST':
        move_name = str(request.POST['move_name'])
        move_single = get_object_or_404(Move, title__iexact=move_name)
        move_single_quote = str(move_single.quote)

        return JsonResponse({"quote": move_single_quote})

    if request.method == 'GET':
        moves = MoveSerializer(
            Move.objects.all().order_by("title"),
            many = True
        ).data

        return JsonResponse({"moves": moves})

#@login_required
def get_sequences(request):
    sequences = SequenceSerializer(
        Sequence.objects.all(),
        many = True
    ).data

    return JsonResponse({"sequences": sequences})
