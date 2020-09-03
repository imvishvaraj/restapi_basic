from rest_framework import serializers

from postings.models import BlogPost



# converts to json
# validates for data passed
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
        read_only_fields = ['pk', 'user']

    def validate_title(self, value):
        qs = BlogPost.objects.filter(title__iexact=value) # include instance

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("This title already used.")

        return value
