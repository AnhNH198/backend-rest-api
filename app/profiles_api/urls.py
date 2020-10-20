from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles_api import views

router = DefaultRouter()
router.register('testviewset', views.TestViewSet, base_name='testviewset')
router.register('profile', views.UserProfileViewSet)

urlpatterns = [
    path('testapiview/', views.TestApiView.as_view()),
    path('', include(router.urls))
]
