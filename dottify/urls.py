# Write your URL patterns here.
from django.contrib import admin
from django.urls import path, include

# from rest_framework import routers  
from rest_framework_nested import routers  
from .views import AlbumDetailView, AlbumDeleteView, SongDeleteView,HomeView, SongDetailView,UserProfileView,AlbumSearchView, AlbumCreateView, SongCreateView, SongUpdateView, AlbumUpdateView
from .api_views import AlbumViewSet, SongViewSet, PlaylistViewSet, NestedSongViewSet, StatisticViewSet

app_name = 'dottify'

router = routers.DefaultRouter()
router.register(r'albums', AlbumViewSet, basename='album-api')
router.register(r'songs', SongViewSet, basename='song')
router.register(r'playlists', PlaylistViewSet, basename='playlist-api')

album_router = routers.NestedDefaultRouter(router, "albums", lookup = "album")
album_router.register(r'songs', NestedSongViewSet, basename="album-api-songs")

urlpatterns = [


    path('', HomeView.as_view(), name = 'home'),

    path('albums/<int:id>/',AlbumDetailView.as_view(), name='album_detail'),
    path('albums/search/', AlbumSearchView.as_view(),name='album_search'),
    path('albums/new/', AlbumCreateView.as_view(), name = "album_create"),
    path('albums/<int:pk>/edit/',AlbumUpdateView.as_view(), name='album_update'),
    path('albums/<int:pk>/delete/',AlbumDeleteView.as_view(), name='album_delete'),
    path('albums/<int:id>/<slug:slug>/',AlbumDetailView.as_view(), name='album_detail_slug'),

    path('songs/<int:pk>/', SongDetailView.as_view(), name = 'song_detail'),
    path('songs/<int:pk>/edit/',SongUpdateView.as_view(), name = 'song_update'),
    path('songs/<int:pk>/delete/',SongDeleteView.as_view(), name = 'song_delete'),
    path('songs/new/', SongCreateView.as_view(), name = 'song_create'),

    path('users/<int:id>/', UserProfileView.as_view(), name = 'user_profile'),
    path('users/<int:id>/<slug:slug>/', UserProfileView.as_view(), name='user_profile_slug'),

    path('api/', include(router.urls)),
    path('api/', include(album_router.urls)),
    path('api/statistics/',StatisticViewSet.as_view(), name="statistics")
]
