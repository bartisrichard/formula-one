from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Car, Rating

from racing import serializers


class BaseRacingAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CarViewSet(BaseRacingAttrViewSet):
    queryset = Car.objects.all()
    serializer_class = serializers.CarSerializer


class RatingViewSet(BaseRacingAttrViewSet):
    queryset = Rating.objects.all()
    serializer_class = serializers.RatingSerializer