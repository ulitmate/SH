from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from . models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        dept = 1
        fields = ['uuid','first_name', 'last_name', 'email', 'telephone',  'password']
        extra_kwargs = {
            'password': {'write_only': True} 
            
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance
    
    