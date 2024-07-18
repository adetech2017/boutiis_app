from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from .models import IcHadithArabic, IcHadithEnglish
from .serializers import IcHadithArabicSerializer, IcHadithEnglishSerializer




class HadithListView(generics.GenericAPIView):
    def get_serializer_class(self):
        language = self.kwargs.get('language', 'arabic')
        if (language == 'english'):
            return IcHadithEnglishSerializer
        return IcHadithArabicSerializer

    def get_queryset(self):
        language = self.kwargs.get('language', 'arabic')
        if (language == 'english'):
            return IcHadithEnglish.objects.all()
        return IcHadithArabic.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)
