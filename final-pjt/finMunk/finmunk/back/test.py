import requests, json
from datetime import date

url = 'https://prod-api.exgold.co.kr/api/v1/main/chart/period/price/international'
params = {
    'type': 'AU',  # Silver
    'from': '2023-01-01',
    'to': date.today().isoformat()
}

res = requests.get(url, params=params)
data = res.json().get('data', [])

with open('gold_chart.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"{len(data)}개 gold 데이터 저장 완료 ✅")
