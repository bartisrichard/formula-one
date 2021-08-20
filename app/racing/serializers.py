from rest_framework import serializers

from core.models import Car, Rating


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ('name', 'enginesupplier', 'performance', 'wear',)
        read_only_fields = ('name',)


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ('name','overall','experience','racecraft','awareness','pace')
        read_only_fields = ('name',)
