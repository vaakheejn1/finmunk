from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Consultation
from .serializers import ConsultationSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_consultation(request):
    serializer = ConsultationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({'message': '상담 신청 완료'})
    return Response(serializer.errors, status=400)
