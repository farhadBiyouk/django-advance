from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from blog.api.v1.serializers import CategorySerializer, PostSerializer
from blog.models import Post, Category
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework import mixins
from rest_framework import viewsets
from blog.api.v1.permissions import IsOwnerObject
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination

data = {"id": 1, "title": "hello"}


@api_view(["GET", "POST"])
@permission_classes(
    [
        IsAuthenticatedOrReadOnly,
    ]
)
def api_get_list_view(request):
    if request.method == "GET":
        posts = Post.objects.all()
        ser = PostSerializer(posts, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        ser = PostSerializer(data=request.POST)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_200_OK)


@api_view(["GET", "PUT", "DELETE"])
def api_get_detail_view(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == "GET":
        ser = PostSerializer(post)
        return Response(ser.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        ser = PostSerializer(instance=post, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        post.delete()
        return Response({"detail": "this item successfully deleted"})


# class PostList(APIView):
#     permission_classes = (IsAuthenticated, )
#     serializer_class = PostSerializer
#     """ getting list of post and creating new post"""

#     def get(self, request):
#         """retrieving  a list of post"""
#         posts = Post.objects.all()
#         ser = PostSerializer(posts, many=True)
#         return Response(ser.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         """ create a new post"""
#         ser = PostSerializer(data=request.POST)
#         ser.is_valid(raise_exception=True)
#         ser.save()
#         return Response(ser.data, status=status.HTTP_200_OK)


class PostList(ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = PostSerializer
    """ getting list of post and creating new post"""


# class PostDetail(APIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = PostSerializer

#     def get(self, request, post_id):
#         post = get_object_or_404(Post, pk=post_id)
#         ser = PostSerializer(post)
#         return Response(ser.data, status=status.HTTP_200_OK)

#     def put(self, request, post_id):
#         post = get_object_or_404(Post, pk=post_id)
#         ser = PostSerializer(post, data=request.data, partial=True)
#         ser.is_valid(raise_exception=True)
#         return Response(ser.data, status=status.HTTP_200_OK)

#     def delete(self, request, post_id):
#         post = get_object_or_404(Post, pk=post_id)
#         post.delete()

# class PostDetail(GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):

#     permission_classes = (IsAuthenticated,)
#     serializer_class = PostSerializer
#     queryset = Post.objects.all()
#     lookup_field = 'pk'

#     # def get(self, request, post_id):
#     #     post = get_object_or_404(Post, pk=post_id)
#     #     ser = self.serializer_class(post)
#     #     return Response(ser.data, status=status.HTTP_200_OK)

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


class PostDetail(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = "pk"


# class PostViewSet(viewsets.ViewSet):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = PostSerializer
#     queryset = Post.objects.all()

#     def list(self, request):
#         ser = self.serializer_class(self.queryset, many=True)
#         return Response(ser.data, status=status.HTTP_200_OK)

#     def retrieve(self, request, pk=None):
#         object = get_object_or_404(self.queryset, pk=pk)
#         ser = self.serializer_class(data=object)
#         return Response(ser.data, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = {
        "author": ["exact"],
        "category": ["exact", "in"],
        "status": ["exact"],
    }
    search_fields = ["content", "title"]
    ordering_fields = ["author", "published_date", "status"]

    @action(methods=["get"], detail=False)
    def get_ok(self, request):
        return Response({"detail": "create extra action for view_set"})


class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
