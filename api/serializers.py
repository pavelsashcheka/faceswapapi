from rest_framework import serializers
from .models import User, ImageProcessing


class UserSerializer(serializers.ModelSerializer):
    birthdate = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'])

    class Meta:
        model = User
        fields = '__all__'


class ImageProcessingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProcessing
        fields = '__all__'
