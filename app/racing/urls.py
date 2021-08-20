from django.urls import path, include
from rest_framework.routers import DefaultRouter

from racing import views


router = DefaultRouter()
router.register('cars', views.CarViewSet)
router.register('ratings', views.RatingViewSet)
router.register('drivers', views.DriverViewSet)

app_name = 'racing'

urlpatterns = [
    path('', include(router.urls))
]
