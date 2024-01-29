from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import IngredientViewSet

router_v1 = DefaultRouter()
router_v1.register('ingredients', IngredientViewSet, basename='ingredient')


urlpatterns = [
    path('', include(router_v1.urls)),
]
