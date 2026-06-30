from django.contrib import admin
from .models import Album, Song, Rating, Comment, Playlist, DottifyUser
# Register your models here.

admin.site.register(DottifyUser)
admin.site.register(Playlist)