from rest_framework import serializers

from .models import User, SearchItem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'created_at', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }


class SearchSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = SearchItem
        fields = ['id', 'city', 'search_date', 'user_id']
    
    def get_user_id(self, obj):
        return obj.history.user.id if obj and obj.history else None