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

    def get(self, request, id=None, format=None, limit=20):
        post = Post.objects.order_by('-datetime')[:limit]
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
                    ContentType.objects.get(model='post'),
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
                request.data['target_type'] = ContentType.objects.get(model='user').id
                request.data['target_id'] = request.data['post']
                comment = serializer.save(user=User.objects.get(id=self.request.user.id))

                if post.allow_submission and 'file' in self.request.FILES:
                    comment.file = self.request.FILES.get('file')
                    comment.save()

                data = {}
                if post.target_type == ContentType.objects.get(model='group',app_label='group'):
                    data['type'] = 'group'
                    data['group_id'] = post.target_id
                    data['group_name'] = Group.objects.get(id=post.target_id).name
                if post.target_type == ContentType.objects.get(model='user'):
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
                    ContentType.objects.get(model='comment'),
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

    def get(self, request, id, limit=20):
        post = ((Post.objects.filter(user=User.objects.get(id=id), target_type=ContentType.objects.get(model='user')) | Post.objects.filter(target_id=id , target_type=ContentType.objects.get(model='user'))).order_by('-datetime'))[:limit]
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

    def get(self, request, action, id, limit=20):

        if action == 'more':
            post = Post.objects.filter(id__lt=id).order_by('-datetime')[:limit]
        if action == 'new':
            post = Post.objects.filter(id__gt=id).order_by('-datetime')
        response = self.serializer_class(post, many=True)
        return Response(response.data)


class UserWallPegination(APIView):
    serializer_class = PostSerializer

    def get(self, request, id, action, post_id, limit=20):
        if action == 'more':
            post = (Post.objects.filter(user=User.objects.get(id=id), target_type=ContentType.objects.get(model='user')) | Post.objects.filter(target_id=id , target_type=ContentType.objects.get(model='user'))).filter(id__lt=post_id).order_by('-datetime')[:limit]
        if action == 'new':
            post = (Post.objects.filter(user=User.objects.get(id=id), target_type=ContentType.objects.get(model='user')) | Post.objects.filter(target_id=id , target_type=ContentType.objects.get(model='user'))).filter(id__gt=post_id).order_by('-datetime')

        response = self.serializer_class(post, many=True)
        return Response(response.data)
