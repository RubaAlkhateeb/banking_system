import os
from rest_framework import serializers
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    account_number = serializers.ReadOnlyField()
    iban = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ('id', 'user_name', 'email', 'password', 'phone', 'account_number', 'iban')

    def create(self, validated_data):

        current_count = User.objects.count() + 1
        account_number = f"{current_count:012d}"
        iban = '{}{}'.format(os.environ.get('IBAN_PREFIX'), account_number)

        user = User.objects.create(
            account_number=account_number,
            iban=iban,
            **validated_data
        )
        user.set_password(validated_data['password'])
        user.save()
        return user