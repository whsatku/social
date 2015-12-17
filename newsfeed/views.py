from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from newsfeed.models import Post
from newsfeed.models import Comment
from group.models import Group
from event.models import Event
from newsfeed.serializer import PostSerializer
from newsfeed.serializer import CommentSerializer
from notification.views import NotificationViewList
from django.contrib.contenttypes.models import ContentType
from rest_framework.renderers import JSONRenderer
from friendship.models import Friend
from group.models import GroupMember
from event.models import EventMember
import json


class PostViewList(APIView):
    """This class is an API for geting newsfeed posts list.
    """
    serializer_class = PostSerializer

    def get(self, request, format=None, limit=20):
        """Get a list of newsfeed post.
        Args:
                request: Django Rest Framework request object.
                format: pattern for Web APIs.
                limit: number of post in list.
        Return:
            List of last #limit post in database.
        """
        user = User.objects.get(id=self.request.user.id)
        group_post = Post.objects.filter(
            target_type=ContentType.objects.get(
                model='group',
                app_label='group'
                ).id,
            target_id__in=GroupMember.objects.filter(
                user=user
                ).values('group_id')
        )
        event_post = Post.objects.filter(
            target_type=ContentType.objects.get(model='event').id,
            target_id__in=EventMember.objects.filter(
                user=user,
                role__gt=0
                ).values('event_id')
        )
        friend_post = Post.objects.filter(
            target_type=ContentType.objects.get(model='user').id,
            target_id__in=Friend.objects.filter(
                from_user=self.request.user.id).values('to_user'),
            user__in=Friend.objects.filter(
                    from_user=self.request.user.id
                ).values('to_user')
            ) | Post.objects.filter(
            target_type=ContentType.objects.get(model='user').id,
            target_id=None,
            user__in=Friend.objects.filter(
                from_user=self.request.user.id
                ).values('to_user')
            )
        user_post = Post.objects.filter(
            user=user,
            target_type=ContentType.objects.get(model='user')
            ) | Post.objects.filter(
            target_id=user.id,
            target_type=ContentType.objects.get(model='user')
            )
        post = (group_post | event_post | friend_post | user_post).order_by(
            '-datetime')[:limit]
        response = self.serializer_class(post, many=True)

        return Response(response.data)

    def post(self, request, format=None):
        """Save post into database and create notification object.
        Args:
                request: Django Rest Framework request object.
                format: pattern for Web APIs.
        Return:

        """
        serializer = PostSerializer(data=request.data)
        notification = NotificationViewList()
        if serializer.is_valid():

            if self.request.user.is_authenticated():
                try:
                    target = User.objects.get(id=request.data['target_id'])
                    serializer.save(
                        user=User.objects.get(id=self.request.user.id),
                        target_name=(target.first_name+' '+target.last_name)
                    )
                except User.DoesNotExist:
                    serializer.save(
                        user=User.objects.get(id=self.request.user.id),
                        target_name=''
                    )
                data = {}
                data['type'] = 'user'
                if request.data['target_id'] is not None:
                    data['user_id'] = request.data['target_id']
                    data['firstname'] = User.objects.get(
                        id=request.data['target_id']
                    ).first_name
                    data['lastname'] = User.objects.get(
                        id=request.data['target_id']
                    ).last_name
                else:
                    data['user_id'] = None
                json_data = json.dumps(data)
                if request.data['target_id'] is not None:
                    notification.add(
                        request.user,
                        request.data,
                        User.objects.filter(
                            id__in=Friend.objects.filter(
                                from_user=self.request.user.id
                            ).values('to_user')),
                        ContentType.objects.get(model='post'),
                        JSONRenderer().render(serializer.data).decode('utf-8'),
                        json_data
                    )
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                    )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostViewDetail(APIView):
    """This class is an API for geting newsfeed posts information.
    """
    serializer_class = PostSerializer

    def get_object(self, id):
        """Get post by id.
        Args:
                id: id of post.
        Return:
            post object.
        """
        try:
            return Post.objects.get(id=id)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, id=None, format=None):
        """Get single post object by id.
        Args:
                request: Django Rest Framework request object.
                id: id of post.
                format: pattern for Web APIs.
        Return:
            Single post object.
        """
        postObject = self.get_object(id)
        response = self.serializer_class(postObject)
        return Response(response.data)

    def delete(self, request, id, format=None):
        """Delete post in daabase.
        Args:
                request: Django Rest Framework request object.
                id: id of post.
                format: pattern for Web APIs.
        Return:

        """
        posts = self.get_object(id)
        posts.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewList(APIView):
    """This class is an API for geting list of comment.
    """
    serializer_class = CommentSerializer

    def get(self, request, id=None, format=None):
        """Get list of all comments in database.
        Args:
                request: Django Rest Framework request object.
                id: id of post.
                format: pattern for Web APIs.
        Return:
            List of comments in database.
        """
        comment = Comment.objects.all()
        response = self.serializer_class(comment, many=True)

        return Response(response.data)

    def post(self, request, format=None):
        """Post comment to a post.
        Args:
                request: Django Rest Framework request object.
                format: pattern for Web APIs.
        Return:

        """
        serializer = CommentSerializer(data=request.data)
        notification = NotificationViewList()

        if serializer.is_valid():
            if self.request.user.is_authenticated():
                post = Post.objects.get(id=request.data['post'])
                request.data['target_type'] = ContentType.objects.get(
                    model='user'
                ).id
                request.data['target_id'] = request.data['post']
                comment = serializer.save(
                    user=User.objects.get(id=self.request.user.id)
                )
                if post.allow_submission and 'file' in self.request.FILES:
                    comment.file = self.request.FILES.get('file')
                    comment.save()

                data = {}
                if post.target_type == ContentType.objects.get(
                    model='group',
                    app_label='group'
                ):
                    data['type'] = 'group'
                    data['group_id'] = post.target_id
                    data['group_name'] = Group.objects.get(
                        id=post.target_id
                    ).name
                if post.target_type == ContentType.objects.get(model='event'):
                    data['type'] = 'event'
                    data['event_id'] = post.target_id
                    data['event_name'] = Event.objects.get(
                        id=post.target_id
                    ).name
                if post.target_type == ContentType.objects.get(model='user'):
                    data['type'] = 'user'
                    if post.target_id is not None:
                        data['user_id'] = post.target_id
                        data['firstname'] = User.objects.get(
                            id=post.target_id
                        ).first_name
                        data['lastname'] = User.objects.get(
                            id=post.target_id
                        ).last_name
                    else:
                        data['user_id'] = None
                json_data = json.dumps(data)
                notification.add(
                    request.user,
                    request.data,
                    define_receiver(request.data['post']),
                    ContentType.objects.get(model='comment'),
                    JSONRenderer().render(serializer.data).decode('utf-8'),
                    json_data
                )
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewDetail(APIView):
    """This class is an API for geting comment of post detail.
    """
    serializer_class = CommentSerializer

    def get_object(self, id):
        """Get comment by id.
        Args:
                request: Django Rest Framework request object.
                id: id of comment.
                format: pattern for Web APIs.
        Return:
            comment object.
        """
        try:
            return Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, id=None, format=None):
        """Get single comment object.
        Args:
                request: Django Rest Framework request object.
                id: id of comment.
                format: pattern for Web APIs.
        Return:
            Single object of comment.
        """
        comment_object = self.get_object(id)
        response = self.serializer_class(comment_object)

        return Response(response.data)

    def delete(self, request, id, format=None):
        """Delete comment from database by id.
        Args:
                request: Django Rest Framework request object.
                id: id of post.
                format: pattern for Web APIs.
        Return:

        """
        comments = self.get_object(id)
        comments.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostComment(APIView):
    """This class is an API for geting list of comment of post.
    """
    serializer_class = CommentSerializer

    def get(self, request, id, format=None):
        """Get list of comments of post.
        Args:
                request: Django Rest Framework request object.
                id: id of post.
                format: pattern for Web APIs.
        Return:
            List of comments of post.
        """
        comment = Comment.objects.filter(post=id)
        response = self.serializer_class(comment, many=True)

        return Response(response.data)


class UserWallDetail(APIView):
    """This class is an API for geting list of post on user wall.
    """
    serializer_class = PostSerializer

    def get(self, request, id, limit=20):
        """Get list of post on user wall.
        Args:
                request: Django Rest Framework request object.
                id: id of user.
                limit: maximum number of posts in list.
        Return:
            List of post on that user wall.
        """
        post = ((Post.objects.filter(
            user=User.objects.get(id=id),
            target_type=ContentType.objects.get(model='user')
            ) | Post.objects.filter(
            target_id=id,
            target_type=ContentType.objects.get(model='user')
            )
        ).order_by('-datetime'))[:limit]
        response = self.serializer_class(post, many=True)
        return Response(response.data)


def define_receiver(post_id):
    """Define the receiver queryset.
        Args:
                post_id: id of post
        Return:
            Set of receiver of that notification.
        """
    rec = set()
    for i in Comment.objects.filter(post=post_id):
        rec.add(i.user.id)
    rec.add(Post.objects.get(id=post_id).user.id)
    if Post.objects.get(
            id=post_id
            ).target_type == ContentType.objects.get(model='user'):
        rec.add(Post.objects.get(id=post_id).target_id)
    return User.objects.filter(id__in=rec)


class PostPagination(APIView):
    """This class is an API for geting list of newer/older post of newsfeed.
    """
    serializer_class = PostSerializer

    def get(self, request, action, id, limit=20):
        """Get list of newer/older post of newsfeed.
        Args:
                request: Django Rest Framework request object.
                action: 'new'/'more' command to get  newer/older post
                id: current id of post.
                limit: maximum number of post in list.
        Return:
            List of newer/older post of newsfeed.
        """
        user = User.objects.get(id=self.request.user.id)
        group_post = Post.objects.filter(
            target_type=ContentType.objects.get(
                model='group',
                app_label='group').id,
            target_id__in=GroupMember.objects.filter(
                user=user
            ).values('group_id')
        )
        event_post = Post.objects.filter(
            target_type=ContentType.objects.get(
                model='event').id,
            target_id__in=EventMember.objects.filter(
                user=user, role__gt=0
                ).values('event_id')
        )
        friend_post = Post.objects.filter(
            target_type=ContentType.objects.get(
                model='user').id,
            target_id__in=Friend.objects.filter(
                from_user=self.request.user.id
                ).values('to_user'),
            user__in=Friend.objects.filter(
                from_user=self.request.user.id
                ).values('to_user')
            ) | Post.objects.filter(
            target_type=ContentType.objects.get(
                model='user').id,
            target_id=None,
            user__in=Friend.objects.filter(
                from_user=self.request.user.id
            ).values('to_user')
        )
        user_post = Post.objects.filter(
            user=user,
            target_type=ContentType.objects.get(model='user')
            ) | Post.objects.filter(
            target_id=user.id,
            target_type=ContentType.objects.get(model='user')
        )
        if action == 'more':
            post = (group_post | event_post | friend_post | user_post).filter(
                id__lt=id).order_by('-datetime')[:limit]
        if action == 'new':
            post = (group_post | event_post | friend_post | user_post).filter(
                id__gt=id).order_by('-datetime')
        response = self.serializer_class(post, many=True)
        return Response(response.data)


class UserWallPegination(APIView):
    """This class is an API for geting list of newer/older post of user wall.
    """
    serializer_class = PostSerializer

    def get(self, request, id, action, post_id, limit=20):
        """Get list of newer/older post of user wall.
        Args:
                request: Django Rest Framework request object.
                action: 'new'/'more' command to get  newer/older post
                id: current id of post.
                limit: maximum number of post in list.
        Return:
            List of newer/older post of user wall.
        """
        if action == 'more':
            post = (Post.objects.filter(
                user=User.objects.get(id=id),
                target_type=ContentType.objects.get(model='user')
                ) | Post.objects.filter(
                target_id=id,
                target_type=ContentType.objects.get(model='user')
            )).filter(id__lt=post_id).order_by('-datetime')[:limit]
        if action == 'new':
            post = (Post.objects.filter(
                user=User.objects.get(id=id),
                target_type=ContentType.objects.get(model='user')
                ) | Post.objects.filter(
                target_id=id,
                target_type=ContentType.objects.get(model='user')
            )).filter(id__gt=post_id).order_by('-datetime')

        response = self.serializer_class(post, many=True)
        return Response(response.data)
