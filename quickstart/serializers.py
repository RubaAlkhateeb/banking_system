import os
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, UserAccount


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    profile = UserAccountSerializer(required=False)
    # account_number = serializers.ReadOnlyField()
    # iban = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'phone', 'profile')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):

        username = validated_data.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('This username is already in use.')

        email = validated_data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email address is already in use.')

        current_count = User.objects.count() + 1
        account_number = f"{current_count:012d}"
        iban = '{}{}'.format(os.environ.get('IBAN_PREFIX'), account_number)
        profile_data = validated_data.pop('profile', {})

        user = User.objects.create(
            **validated_data
        )
        user.set_password(validated_data['password'])
        user.save()

        account = UserAccount.objects.create(user=user, account_number=account_number, iban=iban, **profile_data)
        user.profile = account
        return user
    

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    # class Meta:
    #     model = User
        # fields = ('id', 'username', 'password')

