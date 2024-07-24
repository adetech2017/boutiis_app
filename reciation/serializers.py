from rest_framework import serializers
from .models import IcHadithArabic, IcHadithEnglish, HadithBooksArabic, HadithBooksEnglish







class IcHadithArabicSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=HadithBooksArabic.objects.all(), write_only=True)

    class Meta:
        model = IcHadithArabic
        fields = ['id', 'book', 'book_id', 'hadith_number', 'hadith_text', 'title']

    def validate_hadith_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Hadith number must be numeric.")
        return value


class IcHadithEnglishSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=HadithBooksEnglish.objects.all(), write_only=True)

    class Meta:
        model = IcHadithEnglish
        fields = ['id', 'book', 'book_id', 'hadith_number', 'hadith_text', 'title']

    def validate_hadith_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Hadith number must be numeric.")
        return value


class HadithBooksArabicSerializer(serializers.ModelSerializer):
    hadiths = serializers.SerializerMethodField()

    class Meta:
        model = HadithBooksArabic
        fields = ['id', 'book', 'book_number', 'source', 'hadiths']

    def get_hadiths(self, obj):
        hadiths = IcHadithArabic.objects.filter(book=obj)
        serializer = IcHadithArabicSerializer(hadiths, many=True)
        return serializer.data


class HadithBooksEnglishSerializer(serializers.ModelSerializer):
    hadiths = serializers.SerializerMethodField()

    class Meta:
        model = HadithBooksEnglish
        fields = ['id', 'book', 'book_number', 'source', 'hadiths']

    def get_hadiths(self, obj):
        hadiths = IcHadithEnglish.objects.filter(book=obj)
        serializer = IcHadithEnglishSerializer(hadiths, many=True)
        return serializer.data
