from community.utils import create_follow_notification  # ✅ 꼭 import!
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, UserProfileSerializer
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import User
from rest_framework.parsers import MultiPartParser, FormParser




class UserProfileView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def profile(request):
    user = request.user
    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({'message': '탈퇴 완료'}, status=204)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_follow(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    current_user = request.user

    if target_user == current_user:
        return Response({'message': '자기 자신은 팔로우할 수 없습니다.'}, status=400)

    if target_user in current_user.followings.all():
        current_user.followings.remove(target_user)
        is_following = False
        message = '언팔로우 했습니다.'
    else:
        current_user.followings.add(target_user)
        is_following = True
        message = '팔로우 했습니다.'
        create_follow_notification(current_user, target_user) 

    return Response({
        'message': message,
        'is_following': is_following
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    serializer = UserProfileSerializer(user, context={'request': request})  
    return Response(serializer.data)


