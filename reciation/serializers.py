from rest_framework import serializers
from .models import IcHadithArabic, IcHadithEnglish, HadithBooksArabic, HadithBooksEnglish






class HadithBooksArabicSerializer(serializers.ModelSerializer):
    class Meta:
        model = HadithBooksArabic
        fields = '__all__'


class HadithBooksEnglishSerializer(serializers.ModelSerializer):
    class Meta:
        model = HadithBooksEnglish
        fields = '__all__'


class IcHadithArabicSerializer(serializers.ModelSerializer):
    class Meta:
        model = IcHadithArabic
        fields = ['id', 'book', 'hadith_number', 'hadith_text', 'title']

class HadithBooksArabicDetailsSerializer(serializers.ModelSerializer):
    hadiths = serializers.SerializerMethodField()  # Use SerializerMethodField for dynamic content

    class Meta:
        model = HadithBooksArabic
        fields = ['id', 'book', 'book_number', 'source', 'hadiths']

    def get_hadiths(self, obj):
        # Fetch related hadiths, ordered by ID, and serialize them
        hadiths = IcHadithArabic.objects.filter(book=obj).order_by('id')
        serializer = IcHadithArabicSerializer(hadiths, many=True)
        return serializer.data

class IcHadithEnglishSerializer(serializers.ModelSerializer):
    class Meta:
        model = IcHadithEnglish
        fields = ['id', 'book', 'hadith_number', 'hadith_text', 'title']

class HadithBooksEnglishDetailsSerializer(serializers.ModelSerializer):
    hadiths = IcHadithEnglishSerializer(many=True, read_only=True)

    class Meta:
        model = HadithBooksEnglish
        fields = ['id', 'book', 'book_number', 'source', 'hadiths']
    
    def get_hadiths(self, obj):
        # Fetch related hadiths, ordered by ID, and serialize them
        hadiths = IcHadithEnglish.objects.filter(book=obj).order_by('id')
        serializer = IcHadithEnglishSerializer(hadiths, many=True)
        return serializer.data