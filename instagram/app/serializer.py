from rest_framework import serializers
from app.models import User, Post, PostLike, UserFollow, PostComment

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = "__all__"

    email = serializers.EmailField()
    first_name =  serializers.CharField()
    last_name =  serializers.CharField()
    username =  serializers.CharField()
    password =  serializers.CharField()
    bio = serializers.CharField()

    def create(self, validated_data):
       return User.objects.create(**validated_data)

    

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    title = serializers.CharField()
    description = serializers.CharField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image = serializers.ImageField(required = False)
    video = serializers.FileField(required = False)

    def update(self, instance, validated_data):
        print(validated_data)
        if instance.user.id == validated_data["user"].id:
            return super().update(instance, validated_data)
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = "__all__"


    comment_text = serializers.CharField(max_length=264)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    def save(self, **kwargs):
        print(kwargs)
        self.post = kwargs["post"]
        return super().save(**kwargs)
        
class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

class UserFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = "__all__"

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    follows_id = serializers.PrimaryKeyRelatedField(read_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'bio',
            'post_count', 'follower_count', 'following_count','posts'
        ]

    def get_post_count(self, obj):
        return Post.objects.filter(user=obj).count()

    def get_follower_count(self, obj):
        return UserFollow.objects.filter(follows=obj).count()

    def get_following_count(self, obj):
        return UserFollow.objects.filter(user=obj).count()
    
    def get_posts(self, obj):
        posts = Post.objects.filter(user=obj).order_by('created_at')
        return PostSerializer(posts, many = True).data

        
        






