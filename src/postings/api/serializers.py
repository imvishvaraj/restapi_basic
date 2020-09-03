from rest_framework import serializers

from postings.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model   = BlogPost
        fields  = [
            'pk',
            'user',
            'title',
            'content',
            'timestamp',
        ]

    # converts to json
    # validates for data passed

