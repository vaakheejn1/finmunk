from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta, date
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import requests, os, re, json
from bs4 import BeautifulSoup
from pykrx import stock
from pykrx.stock import get_market_ticker_name
from django.conf import settings
import urllib3

# ---- 전역 설정 ----
CURRENCIES = ['USD', 'JPY', 'EUR', 'CNH', 'GBP']
EXIM_API_KEY = os.getenv("EXCHANGE_API_KEY")
EXIM_URL = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---- 도우미 함수들 ----

def get_recent_trading_day():
    today = datetime.today()
    while True:
        if today.weekday() < 5:
            df = stock.get_index_ohlcv_by_date(today.strftime('%Y%m%d'), today.strftime('%Y%m%d'), "1001")
            if not df.empty:
                return today.strftime('%Y%m%d')
        today -= timedelta(days=1)

def get_kospi_kosdaq():
    try:
        recent_date_str = get_recent_trading_day()
        recent_date = datetime.strptime(recent_date_str, "%Y%m%d")
        kospi = stock.get_index_ohlcv_by_date(recent_date_str, recent_date_str, "1001")
        kosdaq = stock.get_index_ohlcv_by_date(recent_date_str, recent_date_str, "2001")

        kospi_value = kospi['\uc885\uac00'].values[0] if not kospi.empty else None
        kosdaq_value = kosdaq['\uc885\uac00'].values[0] if not kosdaq.empty else None

        return {
            'KOSPI': round(kospi_value, 2) if kospi_value else None,
            'KOSDAQ': round(kosdaq_value, 2) if kosdaq_value else None,
            '기준일자': recent_date
        }
    except Exception as e:
        print(f'📉 PyKrx 오류: {e}')
        return {'KOSPI': None, 'KOSDAQ': None, '기준일자': None}

def get_stock_summary():
    try:
        recent_date_str = get_recent_trading_day()
        price_df = stock.get_market_price_change(recent_date_str, recent_date_str)

        if '종목명' not in price_df.columns:
            price_df.index.name = '종목명'
            price_df = price_df.reset_index()

        top_gainers = price_df.sort_values(by="등락률", ascending=False).head(3)
        top_losers = price_df.sort_values(by="등락률", ascending=True).head(3)

        top_gainers = top_gainers.rename(columns={'종가': '현재가'})[['종목명', '현재가', '등락률']].to_dict(orient='records')
        top_losers = top_losers.rename(columns={'종가': '현재가'})[['종목명', '현재가', '등락률']].to_dict(orient='records')

        cap_df = stock.get_market_cap_by_ticker(recent_date_str)
        cap_df.index.name = '티커'
        cap_df = cap_df.reset_index()
        cap_df['종목명'] = cap_df['티커'].apply(get_market_ticker_name)
        cap_df = cap_df.rename(columns={'종가': '현재가'})
        top30 = cap_df.sort_values(by="시가총액", ascending=False).head(30)
        top30 = top30[['종목명', '현재가', '시가총액']].to_dict(orient='records')

        return {
            'top_gainers': top_gainers,
            'top_losers': top_losers,
            'top30': top30
        }
    except Exception as e:
        print(f"📉 주식정보 오류: {e}")
        return {'top_gainers': [], 'top_losers': [], 'top30': []}

def get_news_list():
    url = "https://finance.naver.com/news/news_list.naver?mode=RANK&section_id=101"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    news_list = []
    seen_links = set()
    for item in soup.select(".newsList li"):
        a_tag = item.select_one("a")
        if a_tag:
            title = a_tag.get_text(strip=True)
            link = "https://finance.naver.com" + a_tag['href']
            if link in seen_links:
                continue
            seen_links.add(link)
            news_list.append({"title": title, "link": link})
        if len(news_list) == 3:
            break
    return news_list

def get_news_content(news_url):
    match = re.search(r'article_id=(\d+)&office_id=(\d+)', news_url)
    if not match:
        return "기사 ID 파싱 실패"
    article_id, office_id = match.groups()
    real_url = f"https://n.news.naver.com/mnews/article/{office_id}/{article_id}"
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://n.news.naver.com/"}
    res = requests.get(real_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    article = soup.find("article")
    return article.get_text(strip=True) if article else "본문 파싱 실패"

def get_closest_exchange_rates(target_date: datetime):
    headers = {"User-Agent": "Mozilla/5.0"}
    for _ in range(7):
        date_str = target_date.strftime("%Y%m%d")
        params = {"authkey": EXIM_API_KEY, "searchdate": date_str, "data": "AP01"}
        try:
            res = requests.get(EXIM_URL, params=params, headers=headers, timeout=10, verify=False)
            data = res.json()
            if data and isinstance(data, list):
                return data
        except Exception as e:
            print(f"환율 API 실패: {e}")
        target_date -= timedelta(days=1)
    return []

def parse_exchange_rates(raw_data):
    result = {}
    for item in raw_data:
        cur_unit_raw = item.get("cur_unit")
        if not cur_unit_raw:
            continue
        cur_unit = cur_unit_raw.replace(" ", "")
        if cur_unit in ["USD", "JPY(100)", "EUR", "CNH", "GBP"]:
            key = "JPY" if "JPY" in cur_unit else cur_unit
            try:
                rate_raw = item.get("deal_bas_r")
                if not rate_raw:
                    continue
                rate = float(rate_raw.replace(",", ""))
                if key == "JPY":
                    rate = round(rate / 100, 2)
                result[key] = round(rate, 2)
            except:
                result[key] = None
    return result

def get_realtime_gold_silver_prices():
    try:
        gold_chart = load_chart_data('gold_chart.json')
        silver_chart = load_chart_data('silver_chart.json')

        latest_gold = gold_chart[-1] if gold_chart else {}
        latest_silver = silver_chart[-1] if silver_chart else {}

        return {
            "gold_price": {
                "metal": "gold",
                "international": latest_gold.get("internationalPrice"),
                "domestic": latest_gold.get("domesticPrice")
            },
            "silver_price": {
                "metal": "silver",
                "international": latest_silver.get("internationalPrice"),
                "domestic": latest_silver.get("domesticPrice")
            }
        }
    except Exception as e:
        print(f"❌ 금/은 시세 가져오기 실패: {e}")
        return {
            "gold_price": {"metal": "gold", "international": None, "domestic": None},
            "silver_price": {"metal": "silver", "international": None, "domestic": None},
            "error": str(e),
        }

def load_chart_data(filename):
    try:
        path = os.path.join(settings.BASE_DIR, 'market', 'data', filename)
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 차트 JSON 로딩 실패: {e}")
        return []

# ---- API View ----

@api_view(['GET'])
@permission_classes([AllowAny])
def product_summary_api(request):
    today = datetime.today()
    yesterday = today - timedelta(days=1)

    raw_data_today = get_closest_exchange_rates(today)
    raw_data_yesterday = get_closest_exchange_rates(yesterday)

    today_rates = parse_exchange_rates(raw_data_today)
    yest_rates = parse_exchange_rates(raw_data_yesterday)

    result = {}
    for currency in CURRENCIES:
        today_rate = today_rates.get(currency)
        yest_rate = yest_rates.get(currency)
        if today_rate is None or yest_rate is None:
            result[currency] = {'today': None, 'diff': None, 'rate': None}
            continue
        diff = round(today_rate - yest_rate, 2)
        rate_change = round((diff / yest_rate) * 100, 2)
        result[currency] = {'today': today_rate, 'diff': diff, 'rate': rate_change}

    kospi_kosdaq = get_kospi_kosdaq()
    stock_data = get_stock_summary()
    news_raw = get_news_list()

    news = []
    for item in news_raw:
        content = get_news_content(item['link'])
        news.append({
            'title': item['title'],
            'link': item['link'],
            'date': today.strftime("%Y.%m.%d"),
            'content': content
        })

    prices = get_realtime_gold_silver_prices()
    gold_chart = load_chart_data('gold_chart.json')
    silver_chart = load_chart_data('silver_chart.json')

    return Response({
        'rates': result,
        'financial_data': kospi_kosdaq,
        'news': news,
        'top_gainers': stock_data['top_gainers'],
        'top_losers': stock_data['top_losers'],
        'top30': stock_data['top30'],
        'gold_price': prices['gold_price'],
        'silver_price': prices['silver_price'],
        'gold_chart': gold_chart,
        'silver_chart': silver_chart,
    })
