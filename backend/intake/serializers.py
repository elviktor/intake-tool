from rest_framework import serializers

from .models import Move, Sequence, SequenceRecord

class MoveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Move
        fields = ("type", "title", "quote")


class SequenceSerializer(serializers.ModelSerializer):

    script = serializers.StringRelatedField(many=False)
    move = serializers.StringRelatedField(many=False)

    class Meta:
        model = Sequence
        fields = ("script", "order_num", "move")


class SequenceRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = SequenceRecord
        fields = "__all__"
