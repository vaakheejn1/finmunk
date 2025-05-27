# products/views.py
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RecommendationRequestSerializer
from .ml.recommend import recommend_products
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import DepositProduct, SavingProduct
from .serializers import DepositProductSerializer, SavingProductSerializer
from rest_framework.permissions import IsAuthenticated

class RecommendProductAPIView(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        user = request.user

        if not all([user.age, user.income, user.assets]) or user.job is None:
            return Response({"error": "유저 정보가 부족합니다. 마이페이지에서 정보를 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 기존 추천 결과 가져오기
        result = recommend_products(
            age=user.age,
            job=user.job,
            monthly_income=user.income,
            assets=user.assets
        )
        
        # 추천된 상품에 실제 DB ID와 찜 상태 추가
        if 'recommended_deposit' in result:
            result['recommended_deposit'] = self.add_product_metadata(
                result['recommended_deposit'], 'deposit', user
            )
        
        if 'recommended_saving' in result:
            result['recommended_saving'] = self.add_product_metadata(
                result['recommended_saving'], 'saving', user
            )
        
        return Response(result)
    
    def add_product_metadata(self, products, product_type, user):
        """추천 상품에 실제 DB ID와 찜 상태 추가"""
        enhanced_products = []
        
        for product in products:
            # 상품명으로 실제 DB 상품 찾기
            if product_type == 'deposit':
                try:
                    db_product = DepositProduct.objects.filter(
                        product_name__icontains=product['상품명'][:10]  # 부분 매칭
                    ).first()
                    
                    if db_product:
                        product['id'] = db_product.id
                        product['isLiked'] = user in db_product.liked_by.all()
                    else:
                        # DB에 없는 경우 임시 ID (실제로는 해당 상품을 DB에 추가해야 함)
                        product['id'] = None
                        product['isLiked'] = False
                        
                except Exception as e:
                    print(f"예금 상품 매칭 실패: {e}")
                    product['id'] = None
                    product['isLiked'] = False
            
            elif product_type == 'saving':
                try:
                    db_product = SavingProduct.objects.filter(
                        product_name__icontains=product['상품명'][:10]  # 부분 매칭
                    ).first()
                    
                    if db_product:
                        product['id'] = db_product.id
                        product['isLiked'] = user in db_product.liked_by.all()
                    else:
                        product['id'] = None
                        product['isLiked'] = False
                        
                except Exception as e:
                    print(f"적금 상품 매칭 실패: {e}")
                    product['id'] = None
                    product['isLiked'] = False
            
            # 찜 관련 상태 초기화
            product['isToggling'] = False
            enhanced_products.append(product)
        
        return enhanced_products


class DepositProductListView(ListAPIView):
    queryset = DepositProduct.objects.all()
    serializer_class = DepositProductSerializer

class SavingProductListView(ListAPIView):
    queryset = SavingProduct.objects.all()
    serializer_class = SavingProductSerializer

class AllProductsAPIView(APIView):
    def get(self, request):
        deposits = DepositProduct.objects.all()
        savings = SavingProduct.objects.all()

        deposit_data = DepositProductSerializer(deposits, many=True).data
        saving_data = SavingProductSerializer(savings, many=True).data

        return Response(deposit_data + saving_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_deposit_like(request, product_id):
    try:
        product = DepositProduct.objects.get(id=product_id)
        user = request.user
        
        if user in product.liked_by.all():
            product.liked_by.remove(user)
            return Response({"message": "찜 취소됨", "liked": False})
        else:
            product.liked_by.add(user)
            return Response({"message": "찜 완료", "liked": True})
            
    except DepositProduct.DoesNotExist:
        return Response({"error": "상품을 찾을 수 없습니다."}, status=404)
    except Exception as e:
        return Response({"error": "찜하기 처리 중 오류가 발생했습니다."}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_saving_like(request, product_id):
    try:
        product = SavingProduct.objects.get(id=product_id)
        user = request.user
        
        if user in product.liked_by.all():
            product.liked_by.remove(user)
            return Response({"message": "찜 취소됨", "liked": False})
        else:
            product.liked_by.add(user)
            return Response({"message": "찜 완료", "liked": True})
            
    except SavingProduct.DoesNotExist:
        return Response({"error": "상품을 찾을 수 없습니다."}, status=404)
    except Exception as e:
        return Response({"error": "찜하기 처리 중 오류가 발생했습니다."}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_products(request):
    user = request.user
    liked_deposits = DepositProduct.objects.filter(liked_by=user)
    liked_savings = SavingProduct.objects.filter(liked_by=user)

    deposit_data = DepositProductSerializer(liked_deposits, many=True).data
    saving_data = SavingProductSerializer(liked_savings, many=True).data

    return Response({
        'deposits': deposit_data,
        'savings': saving_data,
    })

# 찜 상태 확인 API (선택사항)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_deposit_like(request, product_id):
    try:
        product = DepositProduct.objects.get(id=product_id)
        liked = request.user in product.liked_by.all()
        return Response({'liked': liked})
    except DepositProduct.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_saving_like(request, product_id):
    try:
        product = SavingProduct.objects.get(id=product_id)
        liked = request.user in product.liked_by.all()
        return Response({'liked': liked})
    except SavingProduct.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)