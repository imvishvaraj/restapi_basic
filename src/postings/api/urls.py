from django.urls import path

from .views import BlogPostRudView


urlpatterns = [
    path('<pk>', BlogPostRudView.as_view(), name='post-rud'),
]
