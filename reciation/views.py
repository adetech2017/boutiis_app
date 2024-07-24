from django.shortcuts import get_object_or_404
from rest_framework import generics, pagination, response
from .models import HadithBooksArabic, HadithBooksEnglish, IcHadithArabic, IcHadithEnglish
from .serializers import HadithBooksArabicSerializer, HadithBooksEnglishSerializer, IcHadithArabicSerializer, IcHadithEnglishSerializer






class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class HadithBooksArabicDetailView(generics.RetrieveAPIView):
    queryset = HadithBooksArabic.objects.all()
    serializer_class = HadithBooksArabicSerializer
    pagination_class = StandardResultsSetPagination

    def get_object(self):
        book_id = self.kwargs.get("book_id")
        return get_object_or_404(HadithBooksArabic, book_number=book_id)

    def get(self, request, *args, **kwargs):
        book = self.get_object()
        hadiths = IcHadithArabic.objects.filter(book=book)
        page = self.paginate_queryset(hadiths)
        if page is not None:
            hadith_serializer = self.get_paginated_response(IcHadithArabicSerializer(page, many=True).data)
        else:
            hadith_serializer = IcHadithArabicSerializer(hadiths, many=True)

        book_serializer = self.get_serializer(book)
        data = book_serializer.data
        data['hadiths'] = hadith_serializer.data if page is None else hadith_serializer.data['results']
        if page is not None:
            data['pagination'] = hadith_serializer.data['pagination']

        return response.Response(data)


class HadithBooksEnglishDetailView(generics.RetrieveAPIView):
    queryset = HadithBooksEnglish.objects.all()
    serializer_class = HadithBooksEnglishSerializer
    pagination_class = StandardResultsSetPagination

    def get_object(self):
        book_id = self.kwargs.get("book_id")
        return get_object_or_404(HadithBooksEnglish, book_number=book_id)

    def get(self, request, *args, **kwargs):
        book = self.get_object()
        hadiths = IcHadithEnglish.objects.filter(book=book)
        page = self.paginate_queryset(hadiths)
        if page is not None:
            hadith_serializer = self.get_paginated_response(IcHadithEnglishSerializer(page, many=True).data)
        else:
            hadith_serializer = IcHadithEnglishSerializer(hadiths, many=True)

        book_serializer = self.get_serializer(book)
        data = book_serializer.data
        data['hadiths'] = hadith_serializer.data if page is None else hadith_serializer.data['results']
        if page is not None:
            data['pagination'] = hadith_serializer.data['pagination']

        return response.Response(data)


class HadithListView(generics.ListAPIView):
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        language = self.kwargs.get('language', 'arabic')
        if language == 'english':
            return IcHadithEnglishSerializer
        return IcHadithArabicSerializer

    def get_queryset(self):
        language = self.kwargs.get('language', 'arabic')
        if language == 'english':
            return IcHadithEnglish.objects.all()
        return IcHadithArabic.objects.all()
