from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from profiles.api.permissions import IsOwnerOrReadOnly, IsOwnProfileOrReadOnly
from profiles.api.serializers import (ProfileAvatarSerializer,
                                      ProfileSerializer,
                                      ProfileStatusSerializer)
from profiles.models import Profile, ProfileStatus


class AvatarUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileAvatarSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class ProfileViewSet(
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnProfileOrReadOnly]


class ProfileStatusViewset(ModelViewSet):
    queryset = ProfileStatus.objects.all()
    serializer_class = ProfileStatusSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_Create(self, serializer):
        user_profile = self.request.user.profiles
        serializer.save(user_profile=user_profile)
