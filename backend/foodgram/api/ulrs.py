from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import IngredientViewSet, TagViewSet, RecipeViewSet

router_v1 = DefaultRouter()
router_v1.register('ingredients', IngredientViewSet, basename='ingredient')
router_v1.register('tags', TagViewSet, basename='tag')
router_v1.register('recipes', RecipeViewSet, basename='recipe')


urlpatterns = [
    path('', include(router_v1.urls)),
]
