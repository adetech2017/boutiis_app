from django.urls import path
from .views import HadithBooksArabicDetailView, HadithBooksEnglishDetailView, HadithBooksListView, HadithListView




urlpatterns = [
    path('hadiths/books/<str:language>/', HadithBooksListView.as_view(), name='hadith-books-list'),
    path('hadiths/language/<str:language>/', HadithListView.as_view(), name='hadith-list'),
    path('hadiths/arabic/<int:book_id>/', HadithBooksArabicDetailView.as_view(), name='hadith-book-arabic-detail'),
    path('hadiths/english/<int:book_id>/', HadithBooksEnglishDetailView.as_view(), name='hadith-book-english-detail'),
]
