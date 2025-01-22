from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    # get_like_count() 호출하고 객체 생성
    like_count = serializers.SerializerMethodField()
    # get_comments() 호출하고 객체 생성
    comments = serializers.SerializerMethodField()

    # class Meta 오버라이딩
    class Meta:
        # 직렬화할 데이터의 기반이 되는 모델 설정
        model = Post
        # 직렬화 대상 필드 지정
        fields = "__all__"
        # 읽기 전용 필드 지정
        read_only_fields = [
            "author",
        ]

    # obj == Post
    def get_like_count(self, obj):
        # 정참조를 이용해서 Post의 like 테이블과 관련있는 유저의 수를 카운팅
        return obj.like.count()

    def get_comments(self, obj):
        # 역참조를 이용해 post와 관련 있는 Comment테이블의 정보를 다 가져오기기
        comments = obj.comments.all()
        # 쿼리셋셋에서 파이썬 자료구조로 직렬화
        return CommentSerializer(comments, many=True).data


class CommentSerializer(serializers.ModelSerializer):

    # class Meta 오버라이딩
    class Meta:
        # 직렬화할 데이터의 기반이 되는 모델 설정
        model = Comment
        # 직렬화 대상 필드 지정
        fields = "__all__"
        # 읽기 전용 필드 지정
        read_only_fields = [
            "post",
            "author",
        ]
