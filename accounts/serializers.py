from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'last_name', 'last_login', 'date_joined', 'is_active', 'password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError("Password do not match")
        # return super().validate(attrs)
        return attrs

    def create(self, validated_data):

        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password')
        )
        print(f"creater user : ", {user})
        # return super().create(validated_data)
        return user

    # def read(self):
    #     token =
    #     return User.objects.filter(id = token.id)
