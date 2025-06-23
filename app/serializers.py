from rest_framework import serializers
from .models import User

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    # def validate_email(self, value):
    #     if value and User.objects.filter(email=value).exists():
    #         raise serializers.ValidationError("This email is already registered.")
    #     return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            # email=validated_data.get('email', ''),
            role=validated_data['role']
        )


from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'status', 'created_at']

    def validate_name(self, value):
        if self.instance:  # For updates
            if Category.objects.exclude(pk=self.instance.pk).filter(name__iexact=value).exists():
                raise serializers.ValidationError("Another category with this name already exists.")
        else:  # For creation
            if Category.objects.filter(name__iexact=value).exists():
                raise serializers.ValidationError("A category with this name already exists.")
        return value
