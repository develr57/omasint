from django.urls import re_path, include, path
from rest_framework import routers
from .views import AnimaltypeViewSet, BreedViewSet, AnimalViewSet, WeightingViewSet
    # UserViewSet, GroupViewSet


router = routers.DefaultRouter()

# router.register(r'api/v1/users', UserViewSet, basename='users')
# router.register(r'api/v1/groups', GroupViewSet, basename='groups')
router.register(r'api/v1/animaltypes', AnimaltypeViewSet, basename='animaltypes')
router.register(r'api/v1/breeds', BreedViewSet, basename='breeds')
router.register(r'api/v1/animals', AnimalViewSet, basename='animals')
router.register(r'api/v1/weightings', WeightingViewSet, basename='weightings')


urlpatterns = router.urls

urls = [
    path(r'api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

urlpatterns += urls