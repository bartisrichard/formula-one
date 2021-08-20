from rest_framework import serializers

from core.models import Car, Rating, Driver


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


class DriverSerializer(serializers.ModelSerializer):
    rating = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Rating.objects.all()
    )
    car = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Car.objects.all()
    )

    class Meta:
        model = Driver
        fields = ('name', 'salaryinmill', 'nationality', 'car', 'rating')
        read_only_fields = ('name',)


class DriverDetailSerializer(DriverSerializer):
    rating = RatingSerializer(many=True, read_only=True)
    car = CarSerializer(many=True, read_only=True)
