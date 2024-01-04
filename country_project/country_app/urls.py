# myapp/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('users/', CustomUserListView.as_view(), name='customuser-list'),
    path('users/create/', CustomUserCreateView.as_view(), name='customuser-create'),
    path('users/<uuid:pk>/', CustomUserRetrieveUpdateDestroyView.as_view(), name='customuser-retrieve-update-destroy'),
    path('signin/', UserSignInView.as_view(), name='user-signin'),
    path('signout/', UserSignOutView.as_view(), name='user-signout'),

    path('countries/', CountryListCreateAPIView.as_view(), name='country-list'),
    path('countries/<uuid:pk>/', CountryDetailAPIView.as_view(), name='country-detail'),
    path('states/', StateListCreateAPIView.as_view(), name='state-list'),
    path('states/<uuid:pk>/', StateDetailAPIView.as_view(), name='state-detail'),
    path('cities/', CityListCreateAPIView.as_view(), name='city-list'),
    path('cities/<uuid:pk>/', CityDetailAPIView.as_view(), name='city-detail'),
]
