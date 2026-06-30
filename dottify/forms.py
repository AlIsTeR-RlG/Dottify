# Any form helpers should go in this file.
from django import forms
from .models import Album, Song

class AlbumForm(forms.ModelForm):
    class Meta:
        model =  Album
        fields = ['title', 'artist_name', 'retail_price', 'cover_img', 'format', 'release_date']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'})
        }

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'length', 'album']
    
    def __init__(self, *args, **kwargs): 
        self.user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs) 
         
        # If user is Artist, only show their albums 
        if self.user and self.user.groups.filter(name='Artist').exists(): 
            self.fields['album'].queryset = Album.objects.filter( 
                artist_account__user=self.user 
            ) 