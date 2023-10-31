from django.urls import path
from . import views



urlpatterns = [
    # Campaign URLs
    path('campaigns/', views.CampaignListCreateView.as_view(), name='campaign-list'),
    path('campaigns/<int:pk>/', views.CampaignDetailView.as_view(), name='campaign-detail'),

    # Donation URLs
    #path('donations/', views.DonationListCreateView.as_view(), name='donation-list'),
    path('donations/<int:pk>/', views.DonationDetailView.as_view(), name='donation-detail'),

    # Donation Transaction URLs
    path('donation-transactions/', views.DonationTransactionListCreateView.as_view(), name='donation-transaction-list'),
    path('donation-transactions/<int:pk>/', views.DonationTransactionDetailView.as_view(), name='donation-transaction-detail'),

    # User Donation History URLs
    path('user-donation-history/', views.UserDonationHistoryListCreateView.as_view(), name='user-donation-history-list'),
    path('user-donation-history/<int:pk>/', views.UserDonationHistoryDetailView.as_view(), name='user-donation-history-detail'),

    # User Donations List for a Single User
    path('user-donations/', views.UserDonationList.as_view(), name='user-donations-list'),
]

