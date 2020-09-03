# generic
from django.db.models import Q
from rest_framework import generics, mixins

from postings.models import BlogPost
from .permissions import IsOwnerOrReadOnly
from .serializers import BlogPostSerializer


class BlogPostAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    # we are using mixins to provide ablity to list posts as well to edit them
    # it is like combining ListAPIView and CreateAPIView

    lookup_field        = 'pk' # slug, id # (r'?P<pk>\d+')
    serializer_class    = BlogPostSerializer
    # permission_classes  = []          # for permission related with content
    # queryset        = BlogPost.objects.all()
    
    def get_queryset(self):
        # implementing searching in api
        qs = BlogPost.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)
                ).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

    # def patch(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)   



class BlogPostListAPIView(generics.ListAPIView):
    lookup_field        = 'pk' # slug, id # (r'?P<pk>\d+')
    serializer_class    = BlogPostSerializer
    # queryset        = BlogPost.objects.all()
    
    def get_queryset(self):
        return BlogPost.objects.all()



class BlogPostCreateAPIView(generics.CreateAPIView):
    lookup_field        = 'pk' # slug, id # (r'?P<pk>\d+')
    serializer_class    = BlogPostSerializer
    # queryset        = BlogPost.objects.all()
    
    def get_queryset(self):
        return BlogPost.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field        = 'pk' # slug, id # (r'?P<pk>\d+')
    serializer_class    = BlogPostSerializer
    permission_classes  = [IsOwnerOrReadOnly]
    # queryset        = BlogPost.objects.all()
    
    def get_queryset(self):
        return BlogPost.objects.all()
    
    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return BlogPost.objects.all(pk=pk)
