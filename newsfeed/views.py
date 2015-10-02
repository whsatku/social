from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from newsfeed.Serializer import PostSerializer, CommentSerializer
from newsfeed.models import Post


class PostView(APIView):
    serializer_class = PostSerializer

    def get(self, request, id=None, format=None):
        post = Post.objects.all()
        response = self.serializer_class(post, many=True)

        return Response(response.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



