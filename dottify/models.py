from django.db import models
from django.template.defaultfilters import slugify
from django.core.validators import (MaxValueValidator, StepValueValidator,
                                    RegexValidator,MinValueValidator)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.db.models import Count


# Create your models here.
class DottifyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=800,blank=False,null=False)

class Album(models.Model):

    def get_release_date() -> datetime.date:
        return datetime.today() + timedelta(days=180)
    
    class Format(models.TextChoices):
        SNGL = 'SNGL', _('Single')
        RMST = 'RMST', _('Remaster')
        DLUX = 'DLUX', _('Deluxe Edition')
        COMP = 'COMP', _('Compilation')
        LIVE = 'LIVE', _('Live Perfomance')
    
    title = models.CharField(max_length=800, blank=False, null = False)
    cover_img = models.ImageField(default = "no_cover.jpg")
    artist_name = models.CharField(max_length = 800, blank = False, null = False)
    artist_account = models.ForeignKey(DottifyUser, on_delete = models.CASCADE, blank = True, null=True)
    release_date =models.DateField(blank = False, null = False, default=get_release_date)
    retail_price = models.DecimalField(blank = False, validators=[MaxValueValidator(999.99),MinValueValidator(0)], decimal_places=2, max_digits=5)
    format = models.CharField(max_length=800, choices=Format)

    class Meta:
        constraints = [
            models.UniqueConstraint('title', 'artist_name', 
                                    name='unique_list_within_title')
        ]
    
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class Rating(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, default=None)
    date = models.DateField(blank = False, null = False, default=datetime.today())
    stars = models.DecimalField(validators=[MinValueValidator(0), MaxValueValidator(5), StepValueValidator(0.5)], decimal_places=1, max_digits=2)


class Song(models.Model):

    title = models.CharField(max_length=800, blank=False, null = False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, blank = False, null = False)

    class Meta:
        constraints = [
            models.UniqueConstraint('title', 'album', 
                                    name='unique_song_for_al')
        ]

    length = models.IntegerField(validators=[MinValueValidator(10)])
    position = models.PositiveIntegerField(blank = True, null = True)

    def save(self, *args, **kwargs):
        high = (Song.objects.filter(album = self.album)
                .aggregate(models.Max("position",default = 0)).get("position_max"))
        self.position = (high or 0) +1
        return super().save(*args, **kwargs)
    
class Comment(models.Model):

    comment_text = models.TextField()
    song = models.ForeignKey(Song, on_delete = models.CASCADE, blank = True, null=True)
    commenttee = models.ForeignKey(DottifyUser, on_delete = models.CASCADE, blank = True, null=True)
    
class Playlist(models.Model):

    name = models.CharField(max_length=800, blank=False, null = False)
    songs = models.ManyToManyField(Song)

    class Visibility(models.IntegerChoices):
        HIDDEN = 0, _('Hidden')
        UNLISTED = 1, _('Unlisted')
        PUBLIC = 2, _('Public')
    visibility = models.IntegerField(choices=Visibility, default='0')
    owner = models.ForeignKey(DottifyUser, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)