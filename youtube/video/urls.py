from django.urls import path
from video import views


urlpatterns = [
    path('all-videos/', views.AllVideosView.as_view(), name='all videos'),
    path('search/', views.SearchVideoView.as_view(), name='search video'),
]
