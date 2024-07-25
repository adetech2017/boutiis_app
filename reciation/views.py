from django.shortcuts import get_object_or_404
from rest_framework import generics, pagination, response
from .models import HadithBooksArabic, HadithBooksEnglish, IcHadithArabic, IcHadithEnglish
from .serializers import HadithBooksArabicDetailsSerializer, HadithBooksArabicSerializer, HadithBooksEnglishDetailsSerializer, HadithBooksEnglishSerializer, IcHadithArabicSerializer, IcHadithEnglishSerializer






class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class HadithBooksListView(generics.ListAPIView):
    #pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        language = self.kwargs.get('language', 'arabic')
        if language == 'english':
            return HadithBooksEnglishSerializer
        return HadithBooksArabicSerializer

    def get_queryset(self):
        language = self.kwargs.get('language', 'arabic')
        if language == 'english':
            return HadithBooksEnglish.objects.all()
        return HadithBooksArabic.objects.all()


class HadithBooksArabicDetailView(generics.RetrieveAPIView):
    queryset = HadithBooksArabic.objects.all()
    serializer_class = HadithBooksArabicDetailsSerializer
    pagination_class = StandardResultsSetPagination

    def get_object(self):
        book_id = self.kwargs.get("book_id")
        return get_object_or_404(HadithBooksArabic, id=book_id)

    def get(self, request, *args, **kwargs):
        book = self.get_object()
        hadiths = IcHadithArabic.objects.filter(book=book).order_by('id')
        
        # Handle pagination
        page = self.paginate_queryset(hadiths)
        
        if page is not None:
            hadith_serializer = IcHadithArabicSerializer(page, many=True)
            paginated_data = self.get_paginated_response(hadith_serializer.data)
            data = {
                'book': self.get_serializer(book).data,
                #'hadiths': paginated_data.data['results'],  # Paginated hadiths
                'pagination': {
                    'count': paginated_data.data['count'],
                    'next': paginated_data.data['next'],
                    'previous': paginated_data.data['previous'],
                }
            }
        else:
            hadith_serializer = IcHadithArabicSerializer(hadiths, many=True)
            data = {
                'book': self.get_serializer(book).data,
                'hadiths': hadith_serializer.data  # All hadiths without pagination
            }

        return response.Response(data)


class HadithBooksEnglishDetailView(generics.RetrieveAPIView):
    queryset = HadithBooksEnglish.objects.all()
    serializer_class = HadithBooksEnglishDetailsSerializer
    pagination_class = StandardResultsSetPagination

    def get_object(self):
        book_id = self.kwargs.get("book_id")
        return get_object_or_404(HadithBooksEnglish, id=book_id)  # Use id instead of book_number

    def get(self, request, *args, **kwargs):
        book = self.get_object()
        hadiths = IcHadithEnglish.objects.filter(book=book).order_by('id')  # Ordering Hadiths by ID
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
