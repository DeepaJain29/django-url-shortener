from django.urls import path
from . import views

urlpatterns = [
    path('', views.shorten_url , name='shorten_url'),
    path('<str:short_code>/', views.redirect_to_original, name='redirect_to_original')
]
