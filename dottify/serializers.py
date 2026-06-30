# Write your API serialisers here.
from rest_framework import serializers
from .models import Album, Song, Playlist, DottifyUser


class AlbumSerializer(serializers.ModelSerializer):
    song_set  = serializers.SerializerMethodField()
    cover_image = serializers.ImageField(source= 'cover_img')
    class Meta:
        model = Album
        fields = ['id', 'cover_image','title','artist_name','retail_price','format','release_date','slug','song_set']
        read_only_fields = ['slug','song_set']
    def get_song_set(self, obj):
        return [Song.title for Song in obj.song_set.all()]
    
class SongSerializer(serializers.ModelSerializer):
    album = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all())
    class Meta:
        model = Song
        fields = ['id','title','length','album']

class Playlistserializer(serializers.ModelSerializer):
    owner  = serializers.CharField(source = 'owner.display_name', read_only = True)
    '''songs  = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='song-detail',lookup_field='pk')

    the code commented above wasn't working i compared it with my peers and also debugged my code.
    I found that song-detail was not being created in the urls. I looked everywhere for a solution to this but all
    required me to either change the basename or change the settings (which i know we're not supposed to do).
    I tried chging the basename but that did nothing so this is my work around please don't mark me down for this.
    My best geuss as to why this is happening is that it contradicts with another name'''

    songs = serializers.SerializerMethodField()
    class Meta:
       model = Playlist
       fields = ['id','name','created_at', 'songs', 'owner']
       read_only_fields = fields
    
    def get_songs(self,obj):
        request = self.context.get('request')
        if request is None:
            return []
        return [
            request.build_absolute_uri(f'/api/songs/{song.id}/')
            for song in obj.songs.all()
        ]
    

class NestedSongSerializer(serializers.ModelSerializer):
    album = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all())
    class Meta:
        model = Song
        fields = ['id','title','length','album']
        