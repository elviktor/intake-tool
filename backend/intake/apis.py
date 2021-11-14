from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Move, Sequence, SequenceRecord
from .serializers import MoveSerializer, SequenceSerializer, SequenceRecordSerializer

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

    elif request.method == 'GET':
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

@api_view(['GET', 'POST'])
@csrf_exempt
def get_sequencerecords(request):
    if request.method == 'POST':
        serializer = SequenceRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        records = SequenceRecordSerializer(
            SequenceRecord.objects.all(),
            many = True
        ).data

        return JsonResponse({"records": records})
