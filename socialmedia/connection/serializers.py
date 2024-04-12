from rest_framework import serializers

from .models import FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = (
            "sent_by",
            "sent_to",
            "created_at",
            "accepted_at",
            "rejected_at",
            "canceled_at",
            "status",
        )
