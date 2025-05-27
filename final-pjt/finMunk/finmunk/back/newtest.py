import requests
import json
from datetime import datetime

API_KEY = "d9c27676a864ab1f98773301922e0bd5"
BASE_URL = "https://finlife.fss.or.kr/finlifeapi"
TODAY = datetime.today().strftime("%Y%m%d")

def fetch_and_format_products(endpoint, model_name):
    url = f"{BASE_URL}/{endpoint}.json"
    params = {
        "auth": API_KEY,
        "topFinGrpNo": "020000",  # 은행
        "pageNo": 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    result = []
    base_list = data.get('result', {}).get('baseList', [])
    option_list = data.get('result', {}).get('optionList', [])

    for product in base_list:
        product_code = product['fin_prdt_cd']
        related_options = [opt for opt in option_list if opt['fin_prdt_cd'] == product_code]
        for option in related_options:
            result.append({
                "model": model_name,
                "fields": {
                    "bank_name": product.get("kor_co_nm"),
                    "product_name": product.get("fin_prdt_nm"),
                    "join_way": product.get("join_way"),
                    "maturity_type": product.get("mtrt_info"),
                    "join_deny": product.get("join_deny"),
                    "max_limit": product.get("max_limit") if product.get("max_limit") else None,
                    "save_term": option.get("save_trm"),
                    "interest_rate": float(option.get("intr_rate") or 0),
                    "interest_rate2": float(option.get("intr_rate2") or 0)
                }
            })

    return result

deposit_data = fetch_and_format_products("depositProductsSearch", "financial.depositproduct")
saving_data = fetch_and_format_products("savingProductsSearch", "financial.savingproduct")

with open("deposit_products.json", "w", encoding="utf-8") as f:
    json.dump(deposit_data, f, ensure_ascii=False, indent=2)

with open("saving_products.json", "w", encoding="utf-8") as f:
    json.dump(saving_data, f, ensure_ascii=False, indent=2)

print("📦 데이터 저장 완료!")
