from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .convert import do_faceswap
from .email import send_image_via_email
from .models import User, ImageProcessing
from .serializers import UserSerializer, ImageProcessingSerializer


class GetAllUsers(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetSpecialUser(APIView):
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_user(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # def put(self, request, pk):
    #     user = self.get_user(pk)
    #     serializer = UserSerializer(user, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk):
    #     user = self.get_user(pk)
    #     user.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class GetLastRecord(APIView):
    def get(self, request):
        last_image = ImageProcessing.objects.latest('id')
        serializer = ImageProcessingSerializer(last_image)
        return Response(serializer.data)


class PostImage(APIView):
    def get_image(self, pk):
        try:
            return ImageProcessing.objects.get(pk=pk)
        except ImageProcessing.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        image = self.get_image(pk)
        serializer = ImageProcessingSerializer(image)
        return Response(serializer.data)

    def post(self, request):
        serializer = ImageProcessingSerializer(data=request.data)
        if serializer.is_valid():
            background = request.data['background']
            image = request.data['image']
            result_string, result_image = do_faceswap(image, background)
            serializer.validated_data['result_image_string'] = result_string
            serializer.validated_data['result_image'] = result_image
            serializer.save()
            send_image_via_email(request, result_image=result_image, result_string=result_string)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
