from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Todo

User = get_user_model()

class TodoSerializer(serializers.ModelSerializer):

    # def validate_priority(self, priority):
    #     if 10 < priority < 20:
    #         return priority
    #     raise serializers.ValidationError('priority is not OK!')
    
    def validate(self, attrs):
        if 10 < attrs['priority'] < 20:
            return super().validate(attrs)
        raise serializers.ValidationError('priority is not OK!')
    
    class Meta:
        model = Todo
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    todos = TodoSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
