from rest_framework import serializers
from rest_framework.serializers import Serializer


class IsSubscribedMixin(Serializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)


def get_is_subscribed(self, obj):
    request = self.context.get("request")
    if not request or request.user.is_anonymous:
        return False
    return obj.following.filter(
        author=obj, user=request.user
    ).exists()
