from django.urls import path

from .views import BlogPostRudView, BlogPostCreateAPIView, BlogPostListAPIView, BlogPostAPIView


urlpatterns = [
	path('', BlogPostAPIView.as_view(), name='posts'),
	path('list', BlogPostListAPIView.as_view(), name='post-list'),
	path('create', BlogPostCreateAPIView.as_view(), name='post-create'),
    path('<pk>', BlogPostRudView.as_view(), name='post-rud'),
]
