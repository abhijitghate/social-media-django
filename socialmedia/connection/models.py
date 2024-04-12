from datetime import datetime
from django.db import models

from user.models import User


class FriendRequest(models.Model):
    class FriendshipRequestStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        CANCELED = "canceled", "Canceled"

    sent_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_by")
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_to")
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True)
    rejected_at = models.DateTimeField(null=True)
    canceled_at = models.DateTimeField(null=True)
    status = models.CharField(
        max_length=20,
        choices=FriendshipRequestStatus.choices,
        default=FriendshipRequestStatus.PENDING,
    )

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.status == "accepted":
            self.accepted_at = datetime.now()
        if self.status == "rejected":
            self.rejected_at = datetime.now()
        if self.status == "canceled":
            self.canceled_at = datetime.now()
        super(FriendRequest, self).save(*args, **kwargs)
