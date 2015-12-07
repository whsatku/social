from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from newsfeed.models import Post
from newsfeed.models import Comment
from group.models import Group
from newsfeed.serializer import PostSerializer
from newsfeed.serializer import CommentSerializer
from notification.views import NotificationViewList
from django.contrib.contenttypes.models import ContentType
from rest_framework.renderers import JSONRenderer
import json


class PostViewList(APIView):
    serializer_class = PostSerializer

    def get(self, request, id=None, format=None):
        post = Post.objects.order_by('-datetime')
        response = self.serializer_class(post, many=True)

        return Response(response.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        notification = NotificationViewList()
        if serializer.is_valid():

            if self.request.user.is_authenticated():
                serializer.save(user=User.objects.get(id=self.request.user.id))
                data = {}
                data['type'] = 'user'
                if request.data['target_id'] != None:
                    data['user_id'] = request.data['target_id']
                    data['firstname'] = User.objects.get(id=request.data['target_id']).first_name
                    data['lastname'] = User.objects.get(id=request.data['target_id']).last_name
                else:
                    data['user_id'] = None
                json_data = json.dumps(data)
                notification.post(
                    request,
                    User.objects.all(),
                    ContentType.objects.get(id=13),
                    JSONRenderer().render(serializer.data).decode('utf-8'),
                    json_data
                )
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
        notification = NotificationViewList()

        if serializer.is_valid():
            if self.request.user.is_authenticated():
                post = Post.objects.get(id=request.data['post'])
                request.data['target_type'] = 4
                request.data['target_id'] = request.data['post']
                serializer.save(user=User.objects.get(id=self.request.user.id))
                data = {}
                if post.target_type == ContentType.objects.get(id=15):
                    data['type'] = 'group'
                    data['group_id'] = post.target_id
                    data['group_name'] = Group.objects.get(id=post.target_id).name
                if post.target_type == ContentType.objects.get(id=4):
                    data['type'] = 'user'
                    if post.target_id != None:
                        data['user_id'] = post.target_id
                        data['firstname'] = User.objects.get(id=post.target_id).first_name
                        data['lastname'] = User.objects.get(id=post.target_id).last_name
                    else:
                        data['user_id'] = None
                json_data = json.dumps(data)
                notification.post(
                    request,
                    define_receiver(request.data['post']),
                    ContentType.objects.get(id=14),
                    JSONRenderer().render(serializer.data).decode('utf-8'),
                    json_data
                )
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


class PostComment(APIView):
    serializer_class = CommentSerializer

    def get(self, request, id, format=None):
        comment = Comment.objects.filter(post=id)
        response = self.serializer_class(comment, many=True)

        return Response(response.data)


class UserWallDetail(APIView):
    serializer_class = PostSerializer

    def get(self, request, id):
        post = (Post.objects.filter(user=User.objects.get(id=id), target_type=ContentType.objects.get(id=4)) | Post.objects.filter(target_id=id , target_type=ContentType.objects.get(id=4))).order_by('-datetime')
        response = self.serializer_class(post, many=True)
        return Response(response.data)


def define_receiver(post_id):
    rec = set()
    for i in Comment.objects.filter(post=post_id):
        rec.add(i.user.id)
    rec.add(Post.objects.get(id=post_id).user.id)
    return User.objects.filter(id__in=rec)


class PostPagination(APIView):
    serializer_class = PostSerializer

    def get(self, request, action, id):

        if action == 'more':
            post = Post.objects.filter(id__lt=id).order_by('-datetime')[:20]
        if action == 'new':
            post = Post.objects.filter(id__gt=id).order_by('-datetime')
        response = self.serializer_class(post, many=True)
        return Response(response.data)
