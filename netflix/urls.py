from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi

from .views import MovieViewSet, ActorViewSet, MovieActorListAPIView, MovieActorDetailAPIView, CommentCRAPIview, CommentDetailAPIView

schema_view = get_schema_view(
    openapi.Info(
        title='Netflix Pro API',
        default_version='v1',
        description='Test Description',
    ),
    public=True,
    # permission_classes=(AllowAny)
)


router = DefaultRouter()
router.register('v1/movies', MovieViewSet)
router.register('v1/actors', ActorViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('auth/', obtain_auth_token),
    path('movies/', MovieActorListAPIView.as_view()),
    path('movies/<int:pk>/actors/', MovieActorDetailAPIView.as_view()),
    path("comment/", CommentCRAPIview.as_view()),
    path("comment/<int:pk>/", CommentDetailAPIView.as_view()),
    path("swg-docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-docs"),
    path("redoc-docs/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc-docs"),
]