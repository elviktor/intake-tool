from rest_framework import serializers

from .models import Move, Sequence

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
        # To look up the Move based on this serializer's fields?
        # 1) for downloaded Move dictionary - reverse the lowercase and spacing
        #   to perform a JSON key search
        # 2) for API GET request - search by Move key or name
