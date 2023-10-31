from rest_framework import serializers
from .models import Campaign, Donation, DonationTransaction, UserDonationHistory



class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'


class DonationTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationTransaction
        fields = '__all__'


class UserDonationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDonationHistory
        fields = '__all__'