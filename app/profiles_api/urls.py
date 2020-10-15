from django.urls import path

from profiles_api import views


urlpatterns = [
    path('testapiview/', views.TestApiView.as_view())
]
