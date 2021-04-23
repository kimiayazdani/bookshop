from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class BookAd(models.Model):
    CAT_CHOICES = (
        ('FANTASY', 'fantasy'),
        ('BIOGRAPHY', 'biography'),
        ('CLASSIC', 'classic'),
        ('COMMIC', 'commic'),
        ('HORROR', 'horror'),
        ('ROMANCE', 'romance'),
        ('OTHER', 'other'),
    )

    title = models.CharField(max_length=40)
    author = models.CharField(max_length=40)
    price = models.IntegerField(default=10000)
    category = models.CharField(choices=CAT_CHOICES, default='OTHER', max_length=30)
    publication = models.CharField(max_length=50)

    def __str__(self):
        return str(self.title) + ' / ' + str(self.author)

    def get_absolute_url(self):
        return reverse('ad', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(BookAd, self).save(*args, **kwargs)
