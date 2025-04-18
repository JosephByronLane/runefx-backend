from rest_framework import serializers
from django.contrib.auth import get_user_model
import re
import json
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_picture', 'role', 'bio', 'dcc']

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        style={'input_type': 'text'},
        max_length=25,
        min_length=3,
        error_messages={
            'required': 'Username is required',
            'blank': 'Username is required',
            'invalid': 'Username is invalid',
            'min_length': 'Username must be at least 3 characters long',
            'max_length': 'Username must be less than 25 characters long',
        }
    )

    email = serializers.EmailField(
        required=True,
        style={'input_type': 'email'},
        error_messages={
            'required': 'Email is required',
            'blank': 'Email is required',
            'invalid': 'Email is invalid',
        }
    )

    def validate_password(self,value):
        """Function validates if password is strong enough (has at least one uppercase letter, one lowercase letter, one number, and one special character)

        :param value: Password to validate
        :type value: str
        :raises serializers.ValidationError: If password is not strong enough
        :return: Validated password
        :rtype: str
        """
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one number")
        if not re.search(r'[!@#$%^&*()_+]', value):
            raise serializers.ValidationError("Password must contain at least one special character")
        return value

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        error_messages={
            'required': 'Password is required',
            'blank': 'Password is required',
            'invalid': 'Password is invalid',
            'min_length': 'Password must be at least 8 characters long',
        }
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'},
        error_messages={
            'required': 'Password confirmation is required',
            'blank': 'Password confirmation is required',
            'invalid': 'Password confirmation is invalid',
        }
    )

    dcc = serializers.ChoiceField(
        choices=User.DCC_CHOICES,
        required=True,
        style={'input_type': 'text'},
        error_messages={
            'required': 'DCC is required',
            'blank': 'DCC is required',
            'invalid': 'DCC is invalid',
        },

    )
    
    first_name = serializers.CharField(
        required=True,
        style={'input_type': 'text'},
        error_messages={
            'required': 'First name is required',
        }
    )

    last_name = serializers.CharField(
        required=True,
        style={'input_type': 'text'},
        error_messages={
            'required': 'Last name is required',
        }
    )
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name', 'dcc']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"status": "error", "message": "Password fields didn't match."})
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"status": "error", "message": "Email already exists."})
        
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"status": "error", "message": "Username already exists."})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        validated_data['role'] = 'user'
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
        
