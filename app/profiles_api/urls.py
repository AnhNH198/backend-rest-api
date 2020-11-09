from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles_api import views

router = DefaultRouter()
router.register('testviewset', views.TestViewSet, base_name='testviewset')
router.register('profile', views.UserProfileViewSet)
router.register('feed', views.UserProfileFeedViewSet)

app_name = 'profiles_api'

urlpatterns = [
    path('testapiview/', views.TestApiView.as_view()),
    path('login/', views.UserLoginApiView.as_view()),
    path('mahoa/', views.MaHoaVanBan.as_view()),
    path('giaima/', views.GiaiMaVanBan.as_view()),
    path('', include(router.urls))
]
