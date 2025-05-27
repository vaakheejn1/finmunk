import json
import joblib
import os
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances

# 기준 경로
FIXTURE_DIR = os.path.join(os.path.dirname(__file__), '..', 'fixtures')

# JSON 로딩 함수
def load_json(filename, is_deposit=True, job=1, age=25):
    filepath = os.path.join(FIXTURE_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    products = []
    for item in raw_data:
        fields = item['fields']
        try:
            상품명 = fields.get('product_name', '알수없음')

            if job == 0 and ('직장' in 상품명 or '근로자' in 상품명):
                continue
            if age >= 34 and '청년' in 상품명:
                continue

            기간 = int(fields.get('save_term', 12))
            최고금리 = float(fields.get('interest_rate2', 2.0))
            max_limit_raw = fields.get('max_limit')
            max_limit = int(max_limit_raw) if max_limit_raw else "한도없음"

            products.append({
                '상품명': 상품명,
                '기간': 기간,
                '금리': 최고금리,
                '가입한도': max_limit
            })
        except Exception as e:
            print(f"⚠️ 변환 오류: {e}")
            continue
    return products

# 모델 로딩
deposit_model = joblib.load(os.path.join(os.path.dirname(__file__), 'deposit_model.pkl'))
saving_model = joblib.load(os.path.join(os.path.dirname(__file__), 'saving_model.pkl'))

# 추천 함수
def recommend_products(age, job, monthly_income, assets, top_n=5):
    X_input = np.array([[age, job, monthly_income, assets]])

    # 최대 허용 비율 설정
    max_ratio = 0.6 if job == 0 else 0.55

    # 모델 예측
    pred_deposit = deposit_model.predict(X_input)[0]
    pred_saving = saving_model.predict(X_input)[0]

    # 예금
    pred_deposit_months, total_deposit_amount = int(pred_deposit[0]), int(pred_deposit[1])
    pred_deposit_amount = total_deposit_amount // pred_deposit_months
    pred_deposit_amount = max(min(pred_deposit_amount, int(monthly_income * max_ratio)), int(monthly_income * 0.15))

    # 적금
    pred_saving_months, pred_saving_amount = int(pred_saving[0]), int(pred_saving[1])
    pred_saving_amount = max(min(pred_saving_amount, int(monthly_income * max_ratio)), int(monthly_income * 0.15))

    # 상품 로딩
    deposit_raw = load_json('deposit_products.json', is_deposit=True, job=job, age=age)
    saving_raw = load_json('saving_products.json', is_deposit=False, job=job, age=age)

    # 예금 필터링 (총납입금 * 10000 <= 가입한도)
    deposit_df = pd.DataFrame([
        {
            **item,
            '월납입금': pred_deposit_amount,
            '총납입금': pred_deposit_amount * item['기간'],
            '예상이자': int(pred_deposit_amount * item['기간'] * (item['금리'] / 100)),
        }
        for item in deposit_raw
        if item['가입한도'] == "한도없음" or pred_deposit_amount * item['기간'] * 10000 <= item['가입한도']
    ])

    # 적금 필터링 (월납입금 * 10000 <= 가입한도)
    saving_df = pd.DataFrame([
        {
            **item,
            '월납입금': pred_saving_amount,
            '총납입금': pred_saving_amount * item['기간'],
            '예상이자': int(pred_saving_amount * item['기간'] * (item['금리'] / 100)),
        }
        for item in saving_raw
        if item['가입한도'] == "한도없음" or pred_saving_amount * 10000 <= item['가입한도']
    ])

    # 거리 계산
    deposit_distances = euclidean_distances(
        [[pred_deposit_months, pred_deposit_amount]],
        deposit_df[['기간', '월납입금']]
    )[0]
    saving_distances = euclidean_distances(
        [[pred_saving_months, pred_saving_amount]],
        saving_df[['기간', '월납입금']]
    )[0]

    # 추천 상품 Top-N
    deposit_top = deposit_df.iloc[np.argsort(deposit_distances)[:top_n]]
    saving_top = saving_df.iloc[np.argsort(saving_distances)[:top_n]]

    return {
        'predicted_deposit': dict(months=pred_deposit_months, amount=pred_deposit_amount),
        'predicted_saving': dict(months=pred_saving_months, amount=pred_saving_amount),
        'recommended_deposit': deposit_top.to_dict(orient='records'),
        'recommended_saving': saving_top.to_dict(orient='records'),
    }

# 테스트
if __name__ == '__main__':
    result = recommend_products(age=27, job=1, monthly_income=500, assets=1200)

    print("📌 예측값:")
    print("예금 예측:", result['predicted_deposit'])
    print("적금 예측:", result['predicted_saving'])

    print("\n🏦 예금 추천:")
    for item in result['recommended_deposit']:
        print(item)

    print("\n💰 적금 추천:")
    for item in result['recommended_saving']:
        print(item)
