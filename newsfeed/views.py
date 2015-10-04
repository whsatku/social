from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from newsfeed.Serializer import PostSerializer, CommentSerializer
from newsfeed.models import Post


class PostViewList(APIView):
    serializer_class = PostSerializer

    def get(self, request, id=None, format=None):
        post = Post.objects.all()
        response = self.serializer_class(post, many=True)

        return Response(response.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            # serializer.user = self.request.user
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
