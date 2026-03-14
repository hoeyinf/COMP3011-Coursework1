"""
URL configuration for api_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from games import views_api
from oauth2_provider import urls as oauth2_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("rest_framework.urls", namespace="rest_framework")),
    path('api/users/<int:pk>', views_api.UserProfile.as_view(), name="user-detail"),
    path("api/users/<int:pk>/reviews", views_api.UserReviews.as_view(), name="user-reviews"),
    path('api/reviews/<int:pk>', views_api.Reviews.as_view(), name="review-detail"),
    path('api/games/<int:pk>', views_api.Games.as_view(), name="game-detail")
]
