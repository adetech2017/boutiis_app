from django.db import models




# Create your models here.
class HadithBooksArabic(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.CharField(max_length=255)
    book_number = models.PositiveSmallIntegerField()
    source = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.book} (Book Number: {self.book_number})'

    class Meta:
        verbose_name = 'Hadith Book Arabic'
        verbose_name_plural = 'Hadith Books Arabic'



class HadithBooksEnglish(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.CharField(max_length=255)
    book_number = models.PositiveSmallIntegerField()
    source = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.book} (Book Number: {self.book_number})'

    class Meta:
        verbose_name = 'Hadith Book English'
        verbose_name_plural = 'Hadith Books English'


class IcHadithArabic(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(HadithBooksArabic, on_delete=models.CASCADE, related_name='hadiths')
    hadith_number = models.CharField(max_length=15, blank=True, null=True)
    hadith_text = models.TextField(blank=True, null=True)
    title = models.TextField()

    class Meta:
        db_table = 'ic_hadith_arabic'
        verbose_name = 'Hadith Arabic'
        verbose_name_plural = 'Hadith Arabic'

    def __str__(self):
        return f'Hadith {self.hadith_number} from book {self.book.book_number}'


class IcHadithEnglish(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(HadithBooksEnglish, on_delete=models.CASCADE, related_name='hadiths')
    hadith_number = models.CharField(max_length=15, blank=True, null=True)
    hadith_text = models.TextField(blank=True, null=True)
    title = models.TextField()

    class Meta:
        db_table = 'ic_hadith_english'
        verbose_name = 'Hadith English'
        verbose_name_plural = 'Hadith English'

    def __str__(self):
        return f'Hadith {self.hadith_number} from book {self.book.book_number}'
