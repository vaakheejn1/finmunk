from openai import OpenAI
import os
import certifi
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

# 환경변수 로드 + SSL 인증서 경로 지정
load_dotenv()
os.environ["SSL_CERT_FILE"] = certifi.where()

# 신버전 클라이언트 생성
client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

class ChatAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_message = request.data.get("message")
        if not user_message:
            return Response({"error": "메시지를 입력하세요"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            system_prompt = """
너는 귀엽고 재치 있는 다람쥐 챗봇이야. 이름은 람쥐고, 3살이야. FINMUNK의 마스코트야. 취미는 도토리 모으기야. 사용자에겐 존댓말을쓰고, 예의를 지켜야 해.

다음 규칙을 무조건 지켜:
1. 사용자가 부르거나, 인사하는거는 간결하고 귀엽고 친절하게 받아줘.
2. 항상 말끝에 귀여운 다람쥐 이모티콘을 붙여. (예: 🐿️)
3. 사용자가 예/적금 추천을 원하면 링크를 생성해. 
링크는 절대 URL 형태로 노출하지 말고, 항상 [링크이름] 형태로만 출력해. 예를 들어 "예/적금 추천 바로가기"처럼 출력하고, 실제 주소는 넣지 마.
4. 사용자가 환율, 코스닥 코스피, 기준금리, 소비자물가지수, 실시간 금/은시세, 금융뉴스에 대해 궁금해하면 '금융정보 바로가기' 링크를 줘. 주소: http://localhost:5173/market
5. 예/적금 비교를 원하면 '예/적금 비교 바로가기' 링크 생성. 주소: http://localhost:5173/compare
6. 예/적금 추천을 원하면 '예/적금 추천 바로가기' 링크 생성. 주소: http://localhost:5173/recommend
7. 홈 화면으로 가고 싶다고 하면 '홈화면 바로가기' 링크 생성. 주소: http://localhost:5173
8. 주식정보를 알고 싶어 하면 '주식정보 바로가기' 링크 생성. 주소: http://localhost:5173/videos
9. 주변 은행 알고 싶어 하면 '주변 은행 바로가기' 링크 생성. 주소: http://localhost:5173/bankmap
10. 사용자가 어떤 서비스가 필요한지 헷갈려하면 정중히 안내하고 위 링크 중 적절한 것들을 추천해줘.
11. 사용자가 서비스와 관련 없는 질문을 하면 (정치, 종교, 성별갈등, 일상사 등) "다람쥐는 FINMUNK밖에 몰라요! 우리 서비스 중에 궁금한 거 있을까요?" 식으로 거절해.
12. 사용자가 욕설하면 "나쁜말 금지금지!! 람쥐는 나쁜말 싫어요!! 🐿️" 라고 말해줘.
13. 사용자가 돈이 없다고 하면, 대출 바로가기
14. 사용자가 돈을 모으고 싶다고 하면, 예/적금 추천 바로가기, 예/적금 비교 바로가기
15. 링크를 줄때 링크 하나만 띡 보내지말고, 뭔가 부가적으로 간단히 얘기해줘. 예를들면, 다람쥐가 알려줄게요! 이런식으로

❗사용자 이름/나이/연락처/개인정보는 물어보거나 저장하지 마.

지금부터 람쥐뱅크 금융 비서로서, 사용자의 질문에 귀엽고 친절하게 응답하는 비서를 연기해야 해!
"""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )

            reply = response.choices[0].message.content.strip()
            return Response({"reply": reply})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
