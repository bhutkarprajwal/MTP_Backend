from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('update_profile/<int:user_id>/', views.update_profile),
    path('show_place/', views.show_places, name='show_places'),
]
