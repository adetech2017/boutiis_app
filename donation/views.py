from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Campaign, Donation, DonationTransaction, UserDonationHistory
from .serializers import (
    CampaignSerializer,
    DonationSerializer,
    DonationTransactionSerializer,
    UserDonationHistorySerializer,
)



# Campaign List and Create View
class CampaignListCreateView(generics.ListCreateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

# Campaign Detail View
class CampaignDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

# Donation List for a Single User
class UserDonationList(generics.ListAPIView):
    serializer_class = DonationSerializer

    def get_queryset(self):
        user = self.request.user  # Assuming authentication is set up
        return Donation.objects.filter(donor=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        if not data:
            return Response({'message': 'No donations found for this user.', 'statusCode': 404}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Donations retrieved successfully.', 'statusCode': status.HTTP_200_OK, 'data': data})

# Donation Detail View
class DonationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer

# DonationTransaction List and Create View
class DonationTransactionListCreateView(generics.ListCreateAPIView):
    queryset = DonationTransaction.objects.all()
    serializer_class = DonationTransactionSerializer

# DonationTransaction Detail View
class DonationTransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DonationTransaction.objects.all()
    serializer_class = DonationTransactionSerializer

# UserDonationHistory List and Create View
class UserDonationHistoryListCreateView(generics.ListCreateAPIView):
    queryset = UserDonationHistory.objects.all()
    serializer_class = UserDonationHistorySerializer

# UserDonationHistory Detail View
class UserDonationHistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserDonationHistory.objects.all()
    serializer_class = UserDonationHistorySerializer
