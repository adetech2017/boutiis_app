from django.urls import path
from .views import HadithListView




urlpatterns = [
    path('hadiths/', HadithListView.as_view(), name='hadith-list-default'),
    path('hadiths/<str:language>/', HadithListView.as_view(), name='hadith-list'),
]
