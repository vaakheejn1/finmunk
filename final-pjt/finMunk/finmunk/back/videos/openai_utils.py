import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

# ✅ 추가: SSL 인증서 우회를 위한 httpx
import httpx
from openai import OpenAI

load_dotenv()

# ✅ SSL 인증서 검사 비활성화 (개발환경 한정)
transport = httpx.HTTPTransport(verify=False)
custom_http_client = httpx.Client(transport=transport)

client = OpenAI(
    api_key=os.getenv("OPEN_AI_API_KEY"),
    http_client=custom_http_client
)

def get_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = ' '.join([line['text'] for line in transcript])
        return text
    except Exception as e:
        return None

def summarize_stock_market(stock_data):
    prompt = f"""
📈 다음은 오늘의 주식 시장 데이터야:

- 상승률 상위 TOP 10: {stock_data['top_gainers']}
- 하락률 하위 TOP 10: {stock_data['top_losers']}
- 시가총액 상위 TOP 30: {stock_data['top30']}

너는 초보자에게 친절하게 설명하는 투자 전문가야.

✅ 출력 형식 가이드 (중요!)
- 반드시 마크다운 형식 사용
- **줄바꿈을 충분히 써서 시각적으로 예쁘게 보여줘**
- 종목명은 출력하지 말고 분석만 반영해
- 이모지 + 굵은 텍스트 활용
- 총 5~7문단 (각 문단마다 한 줄 띄움), 문단마다 2줄 이상은 써줘.

🎯 예시:
📊 **오늘의 주식 시장 요약**

🔺 상승 요약  
...

🔻 하락 요약  
...

🏦 시가총액  
...

💡 투자심리  
...

이 형식 그대로 결과를 마크다운 텍스트로 써줘!
"""


    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )

    return response.choices[0].message.content.strip()

def summarize_youtube_transcript(transcript_text):
    prompt = f"""
🔽 아래는 유튜브 영상의 전체 자막입니다. 이 내용을 **일반 사용자에게 핵심만 전달하는 뉴스 요약 형식**으로 바꿔줘.

✅ 요약 규칙:
1. 전체 자막을 기반으로 **핵심 정보 3~5줄 이내로 요약**해.
2. **인삿말, 유튜브스러운 멘트, 반복 표현, 구독 유도 멘트 등은 제거**해.
3. 말투는 **친절하지만 간결하게**. 존댓말로 마무리해줘.
4. 줄바꿈과 문단 나눔을 **자연스럽게 표시**하고, **내용의 흐름**이 잘 보이도록 구성해.

🎯 자막:
{transcript_text}
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=1000
    )

    return response.choices[0].message.content.strip()
