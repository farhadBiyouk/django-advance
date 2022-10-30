from accounts.models import Profile
from blog.models import Category, Post
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name',)


class PostSerializer(serializers.ModelSerializer):

    snippet = serializers.ReadOnlyField(source='get_snippet')
    relative_url = serializers.URLField(
        source='get_absolute_api_url', read_only=True)
    absolute_url = serializers.SerializerMethodField(read_only=True)
    category = serializers.SlugRelatedField(
        many=False, read_only=False, slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = ('id', 'image', 'author', 'title', 'content', 'snippet', 'category',
                  'status', 'relative_url', 'absolute_url', 'created_date', 'published_date')
        read_only_fields = ('author',)

    def get_absolute_url(self, object):
        request = self.context.get('request')
        return request.build_absolute_uri(object.pk)

    def to_representation(self, instance):
        rep = super().to_representation(instance)  # return a dictionary
        request = self.context.get('request')
        rep['category'] = CategorySerializer(
            instance.category, context={'request': request}).data

        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('snippet', None)
            rep.pop('relative_url', None)
            rep.pop('absolute_url', None)
        else:
            rep.pop('content', None)

        return rep

    def create(self, validated_data):
        validated_data['author'] = Profile.objects.get(
            user__id=self.context.get('request').user.id)
        return super().create(validated_data)
