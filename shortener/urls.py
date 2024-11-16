# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.shorten_url , name='shorten_url'),
#     path('<str:short_code>/', views.redirect_to_original, name='redirect_to_original')
# ]

from django.urls import path
from .views import create_short_url, redirect_view, analytics, URLShortenerAPI

urlpatterns = [
    path("", create_short_url, name="home"),
    path("analytics/", analytics, name="analytics"),  # Place specific paths first
    path("<str:short_code>/", redirect_view, name="redirect"),
    path("api/shorten/", URLShortenerAPI.as_view(), name="api-shorten"),
    path("api/shorten/<str:short_code>/", URLShortenerAPI.as_view(), name="api-get"),
]