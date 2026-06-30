from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.views.generic import DetailView,ListView, CreateView
from django.views.generic.edit import UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden, HttpResponse
from django.utils import timezone
from django.db.models import Avg
from datetime import timedelta
from .models import Album, Song, DottifyUser, Playlist
from .forms import AlbumForm, SongForm

def is_a_or_a(user):
    return user.is_authenticated and (user.groups.filter(name='DottifyAdmin').exists() or user.groups.filter(name='Artist').exists())

class AlbumDetailView(DetailView):
    model = Album
    template_name = 'dottify/album_detail.html'
    context_object_name = 'album'

    def get_object(self):
        return get_object_or_404(Album, id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        album = self.object
        trty_days = timezone.now() - timedelta(days=30)
        rating = album.rating_set.filter(date__gte=trty_days)
        if rating.exists():
            context["recent_avg"]=rating
        else:
            context["recent_avg"]=None
        average = album.rating_set.aggregate(Avg('stars'))['stars__avg']
        context["avg_rat"] = average or 0
        return context

class HomeView(ListView):
    template_name = 'dottify/home.html'
    context_object_name = 'items'

    def get_queryset(self):

        user = self.request.user
        if user.is_authenticated and user.groups.filter(name = 'DottifyAdmin').exists():
            return {
                'albums':Album.objects.all(),
                'playlists':Playlist.objects.all(),
                'songs':Song.objects.all()
                }
        
        elif user.is_authenticated and user.groups.filter(name = 'Artist').exists():
            try:
                dottify_user = user.dottifyuser
                return {
                    'albums':Album.objects.filter(artist_account = dottify_user),
                    'playlists':None,
                    'songs':None
                }
            except DottifyUser.DoesNotExist:
                return {
                    'albums':None,
                    'playlists':None,
                    'songs':None
                }
        elif user.is_authenticated:
            try:
                dottify_user = user.dottifyuser
                return {
                    'albums':None,
                    'playlists':dottify_user.playlist_set.all(),
                    'songs':None
                }
            except DottifyUser.DoesNotExist:
                return {
                    'albums':None,
                    'playlists':None,
                    'songs':None
                }
        else:
            return {
            'albums':Album.objects.all(),
            'playlists':Playlist.objects.filter(visibility = 2),
            'songs':None
            }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total = Song.objects.count()
        context["total_song"] = total
        return context

class SongDetailView(DetailView):
    model = Song
    template_name = 'dottify/song_detail.html'
    context_object_name = 'song'

    def get_object(self):
        return get_object_or_404(Song, id=self.kwargs['pk'])
    
class UserProfileView(DetailView):
    model = DottifyUser
    template_name = 'dottify/user_profile.html'
    context_object_name = 'dottify_user'

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('id')
        d_name_slug = self.kwargs.get('slug', '')
        user = get_object_or_404(DottifyUser, id = user_id)
        c_slug = slugify(user.display_name)

        if d_name_slug != c_slug:
            return redirect('dottify:user_profile_slug', id = user_id, slug= c_slug)
        return super().get(request, *args, **kwargs)
    
    def get_object(self):
        return get_object_or_404(DottifyUser, id=self.kwargs['id'])
    
class AlbumSearchView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Album
    template_name = 'dottify/album_search.html'
    context_object_name = 'albums'

    def test_func(self):
        return True
    
    def handle_no_permission(self):
        return HttpResponse('Must be logged in', status = 401)

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Album.objects.filter(title = query)
        return Album.objects.none()
    
class AlbumCreateView(UserPassesTestMixin,CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'dottify/album_form.html'
    
    def test_func(self):
        return is_a_or_a(self.request.user)
    
    def handle_no_permisions(self):
        return HttpResponseForbidden("403 you don't have permission to make an album")
    
    def form_valid(self, form):
        if self.request.user.groups.filter(name='Artist').exists():
            form.instance.artist_account = self.request.user.dottifyuser
        return super().form_valid(form)
    
    success_url = reverse_lazy('dottify:home')

class SongCreateView(UserPassesTestMixin,CreateView):
    model = Song
    form_class = SongForm
    template_name = 'dottify/song_form.html'
    def test_func(self):
        return is_a_or_a(self.request.user)
    
    def handle_no_permisions(self):
        return HttpResponseForbidden("403 you don't have permission to make a song")
    
    def form_valid(self, form):
        album = form.cleaned_data.get('album')
        if self.request.user.groups.filter(name='Artist').exists():
            if album.artist_account != self.request.user:
                return HttpResponseForbidden("403 you don't have permission to add a song to this album")   
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs =  super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    success_url = reverse_lazy('dottify:home')

class AlbumUpdateView(UserPassesTestMixin,UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'dottify/album_form.html'

    def test_func(self):
        user = self.request.user
        album = self.get_object()

        if user.groups.filter(name = 'DottifyAdmin').exists():
            return True
        
        if user.groups.filter(name = 'Artist').exists():
            if album.artist_account and album.artist_account == user:
                return True
        
        return False

    def handle_no_permisions(self):
        return HttpResponseForbidden("403 you don't have permission to update this album")
    

    success_url = reverse_lazy('dottify:home')

class SongUpdateView(UserPassesTestMixin,UpdateView):
    model = Song
    form_class = SongForm
    template_name = 'dottify/song_form.html'

    def test_func(self):
        user = self.request.user
        song = self.get_object()

        if user.groups.filter(name = 'DottifyAdmin').exists():
            return True
        
        if user.groups.filter(name = 'Artist').exists():
            if song.album.artist_account and song.album.artist_account == user:
                return True
        
        return False

    def handle_no_permisions(self):
        return HttpResponseForbidden("403 you don't have permission to update this song")
    success_url = reverse_lazy('dottify:home')

class AlbumDeleteView(UserPassesTestMixin,DeleteView):
    model = Album
    template_name = 'dottify/album_delete.html'
    def test_func(self):
        user = self.request.user
        album = self.get_object()

        if user.groups.filter(name = 'DottifyAdmin').exists():
            return True
        
        if user.groups.filter(name = 'Artist').exists():
            if album.artist_account and album.artist_account == user:
                return True
        
        return False

    def handle_no_permisions(self):
        return HttpResponseForbidden("403 you don't have permission to delete this album")

    success_url = reverse_lazy('dottify:home')

class SongDeleteView(UserPassesTestMixin,DeleteView):
    model = Song
    template_name = 'dottify/song_delete.html'
    def test_func(self):
        user = self.request.user
        song = self.get_object()

        if user.groups.filter(name = 'DottifyAdmin').exists():
            return True
        
        if user.groups.filter(name = 'Artist').exists():
            if song.album.artist_account and song.album.artist_account == user:
                return True
        
        return False

    def handle_no_permisions(self):
        return HttpResponseForbidden("403 you don't have permission to delete this song")
    success_url = reverse_lazy('dottify:home')

