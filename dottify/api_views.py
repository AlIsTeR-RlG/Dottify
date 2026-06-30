# Use this file for your API viewsets only
# E.g., from rest_framework import ...
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.db.models import Avg
from .models import Album, Song, Playlist, DottifyUser
from .serializers import AlbumSerializer, SongSerializer, Playlistserializer, NestedSongSerializer

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    lookup_field = 'pk'

class PlaylistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = Playlistserializer

    def get_queryset(self):
        return Playlist.objects.filter(visibility=2)
    
class NestedSongViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NestedSongSerializer

    def get_queryset(self):
        album_id = self.kwargs["album_pk"]
        return Song.objects.filter(album = album_id)
    
    def retrieve(self, request, *args, **kwargs):
        song = get_object_or_404(Song, pk = kwargs["pk"], album_id = kwargs["album_pk"])
        return Response(self.get_serializer(song).data)
    
class StatisticViewSet(APIView):
    def get(self, request):
        user_count = DottifyUser.objects.count()
        album_count = Album.objects.count()
        playlist_count = Playlist.objects.filter(visibility = 2).count()
        avg_data = Song.objects.aggregate(Avg("length"))
        song_length_average = avg_data["length__avg"]

        return Response({
            "user_count": user_count,
            "album_count": album_count,
            "playlist_count": playlist_count,
            "song_length_average": song_length_average
        })
# Create your views here.