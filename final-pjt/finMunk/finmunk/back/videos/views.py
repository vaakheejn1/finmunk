import os
import requests
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from .models import SavedVideo
import json
from django.utils.dateparse import parse_datetime
from pykrx import stock
from pykrx.stock import get_market_ticker_name
from datetime import datetime, timedelta
from .openai_utils import get_youtube_transcript, summarize_youtube_transcript, summarize_stock_market

load_dotenv()
logger = logging.getLogger(__name__)

def youtube_search(request):
    q = request.GET.get('q', '')
    api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        logger.error("❌ YOUTUBE_API_KEY 환경변수가 없습니다.")
        return JsonResponse({'error': 'API key not found'}, status=500)

    if not q:
        return JsonResponse({'error': '검색어를 입력하세요.'}, status=400)

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'maxResults': 18,
        'q': q,
        'key': api_key,
        'type': 'video'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return JsonResponse(response.json(), safe=False)
    except requests.exceptions.RequestException as e:
        logger.error(f"유튜브 API 요청 실패: {e}")
        return JsonResponse({'error': '유튜브 API 요청 중 오류가 발생했습니다.'}, status=500)

def saved_videos(request):
    videos = SavedVideo.objects.all().values()
    return JsonResponse({'videos': list(videos)})

@csrf_exempt
def save_or_delete_video(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            video_id = data.get('videoId')
            snippet = data.get('snippet', {})

            if SavedVideo.objects.filter(video_id=video_id).exists():
                return JsonResponse({'message': '이미 저장된 영상입니다.'})

            video = SavedVideo(
                video_id=video_id,
                title=snippet.get('title', ''),
                description=snippet.get('description', ''),
                thumbnail_url=snippet.get('thumbnails', {}).get('medium', {}).get('url', ''),
                published_at=parse_datetime(snippet.get('publishedAt'))
            )
            video.save()
            return JsonResponse({'message': '영상이 저장되었습니다.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            video_id = data.get('videoId')
            video = SavedVideo.objects.filter(video_id=video_id).first()
            if video:
                video.delete()
                return JsonResponse({'message': '영상이 삭제되었습니다.'})
            else:
                return JsonResponse({'message': '해당 영상이 존재하지 않습니다.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': '지원하지 않는 메서드입니다.'}, status=405)

def get_latest_business_day():
    today = datetime.today()

    # 1. 오전 9시 전이면 무조건 전날로 (시간 우선)
    if today.hour < 9:
        today -= timedelta(days=1)

    # 2. 토요일이면 금요일로
    if today.weekday() == 5:  # Saturday
        today -= timedelta(days=1)

    # 3. 일요일이면 금요일로
    elif today.weekday() == 6:  # Sunday
        today -= timedelta(days=2)

    return today.strftime('%Y%m%d'), today != datetime.today()

@csrf_exempt
def stock_summary_for_video(request):
    try:
        date_str, used_backup = get_latest_business_day()  # 📅 평일 보정!

        price_df = stock.get_market_price_change(date_str, date_str)
        if '종목명' not in price_df.columns:
            price_df.index.name = '종목명'
            price_df = price_df.reset_index()

        top_gainers = price_df.sort_values(by="등락률", ascending=False).head(10)
        top_losers = price_df.sort_values(by="등락률", ascending=True).head(10)

        top_gainers = top_gainers.rename(columns={'종가': '현재가'})[['종목명', '현재가', '등락률']].to_dict(orient='records')
        top_losers = top_losers.rename(columns={'종가': '현재가'})[['종목명', '현재가', '등락률']].to_dict(orient='records')

        cap_df = stock.get_market_cap_by_ticker(date_str)
        cap_df.index.name = '티커'
        cap_df = cap_df.reset_index()
        cap_df['종목명'] = cap_df['티커'].apply(get_market_ticker_name)
        cap_df = cap_df.rename(columns={'종가': '현재가'})
        top30 = cap_df.sort_values(by="시가총액", ascending=False).head(30)
        top30 = top30[['종목명', '현재가', '시가총액']].to_dict(orient='records')

        try:
            ai_summary = summarize_stock_market({
                'top_gainers': top_gainers,
                'top_losers': top_losers,
                'top30': top30
            })
        except Exception as e:
            logger.error(f"🔥 ChatGPT 요약 실패: {e}")
            ai_summary = "ChatGPT 요약 실패"

        if used_backup:
            ai_summary = f"📊 오늘은 장이 열리지 않아서 {date_str} 기준 데이터를 보여줄게!\n" + ai_summary

        return JsonResponse({
            'top_gainers': top_gainers,
            'top_losers': top_losers,
            'top30': top30,
            'ai_summary': ai_summary
        }, json_dumps_params={'ensure_ascii': False})

    except Exception as e:
        logger.error(f"📉 stock_summary_for_video 오류: {e}")
        return JsonResponse({
            'top_gainers': [],
            'top_losers': [],
            'top30': [],
            'ai_summary': '요약 실패'
        }, status=500, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def summarize_video_by_id(request):
    video_id = request.GET.get('video_id')
    title = request.GET.get('title', '')
    description = request.GET.get('description', '')

    if not video_id:
        return JsonResponse({'error': 'video_id가 필요합니다.'}, status=400)

    try:
        transcript = get_youtube_transcript(video_id)

        if transcript:
            summary = summarize_youtube_transcript(transcript)
        elif title or description:
            combined = f"제목: {title}\n설명: {description}"
            summary = summarize_youtube_transcript(combined)
        else:
            summary = "제목, 설명, 자막이 모두 없어 요약할 수 없습니다."

    except Exception as e:
        logger.error(f"🔥 유튜브 요약 실패: {e}")
        summary = "요약 실패"

    return JsonResponse({'summary': summary}, json_dumps_params={'ensure_ascii': False})


