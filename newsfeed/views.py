from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from newsfeed.models import Post
from newsfeed.models import Comment
from newsfeed.serializer import PostSerializer
from newsfeed.serializer import CommentSerializer


class PostViewList(APIView):
    serializer_class = PostSerializer

    def get(self, request, id=None, format=None):
        post = Post.objects.all()
        response = self.serializer_class(post, many=True)

        return Response(response.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():

            if self.request.user.is_authenticated():
                serializer.save(user=User.objects.get(id=self.request.user.id))
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostViewDetail(APIView):
    serializer_class = PostSerializer

    def get_object(self, id):
        try:
            return Post.objects.get(id=id)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, id=None, format=None):

        postObject = self.get_object(id)
        response = self.serializer_class(postObject)

        return Response(response.data)

    def delete(self, request, id, format=None):
        posts = self.get_object(id)
        posts.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewList(APIView):
    serializer_class = CommentSerializer

    def get(self, request, id=None, format=None):
        comment = Comment.objects.all()
        response = self.serializer_class(comment, many=True)

        return Response(response.data)

    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            # serializer.user = self.request.user
            serializer.save(user=User.objects.get(id=self.request.user.id))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewDetail(APIView):
    serializer_class = CommentSerializer

    def get_object(self, id):
        try:
            return Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, id=None, format=None):

        comment_object = self.get_object(id)
        response = self.serializer_class(comment_object)

        return Response(response.data)

    def delete(self, request, id, format=None):
        comments = self.get_object(id)
        comments.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
