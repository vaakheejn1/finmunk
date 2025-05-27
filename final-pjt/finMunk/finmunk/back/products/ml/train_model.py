import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor

# CSV 경로
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'User_dummy_data_v2.csv')
df = pd.read_csv(DATA_PATH)

# 입력(X), 출력(Y)
X = df[['age', 'job', 'monthly_income', 'assets']]
y_deposit = df[['deposit_months', 'deposit_amount']]
y_saving = df[['saving_months', 'saving_amount']]

# train/test 분리
X_train, X_test, y_deposit_train, y_deposit_test = train_test_split(X, y_deposit, test_size=0.2, random_state=42)
_, _, y_saving_train, y_saving_test = train_test_split(X, y_saving, test_size=0.2, random_state=42)

# 모델 후보
models = {
    "RandomForest": MultiOutputRegressor(RandomForestRegressor(n_estimators=200, random_state=42)),
    "GradientBoosting": MultiOutputRegressor(GradientBoostingRegressor(n_estimators=200, random_state=42)),
    "Ridge": MultiOutputRegressor(Ridge()),
    "XGBoost": MultiOutputRegressor(XGBRegressor(n_estimators=200, random_state=42, verbosity=0)),
    "LightGBM": MultiOutputRegressor(LGBMRegressor(n_estimators=200, random_state=42, verbose=-1)),
    "CatBoost": MultiOutputRegressor(CatBoostRegressor(iterations=200, random_state=42, verbose=0))
}

results = []

# 학습 및 평가
for name, model in models.items():
    print(f"\n{name} 모델 평가 중...")

    # 예금
    model.fit(X_train, y_deposit_train)
    pred_deposit = model.predict(X_test)
    deposit_rmse = np.sqrt(mean_squared_error(y_deposit_test, pred_deposit))
    deposit_mae = mean_absolute_error(y_deposit_test, pred_deposit)
    deposit_r2 = r2_score(y_deposit_test, pred_deposit)

    # 적금
    model.fit(X_train, y_saving_train)
    pred_saving = model.predict(X_test)
    saving_rmse = np.sqrt(mean_squared_error(y_saving_test, pred_saving))
    saving_mae = mean_absolute_error(y_saving_test, pred_saving)
    saving_r2 = r2_score(y_saving_test, pred_saving)

    print(f"[예금] RMSE: {deposit_rmse:.2f}, MAE: {deposit_mae:.2f}, R²: {deposit_r2:.4f}")
    print(f"[적금] RMSE: {saving_rmse:.2f}, MAE: {saving_mae:.2f}, R²: {saving_r2:.4f}")

    results.append({
        "model": name,
        "deposit_rmse": deposit_rmse,
        "deposit_mae": deposit_mae,
        "deposit_r2": deposit_r2,
        "saving_rmse": saving_rmse,
        "saving_mae": saving_mae,
        "saving_r2": saving_r2
    })

# 결과 출력
results_df = pd.DataFrame(results)
print("\n📊 전체 모델 비교:")
print(results_df)

# 최고 성능 모델 선택 (예금 RMSE, 적금 RMSE 기준)
best_deposit_model_name = results_df.sort_values(by='deposit_rmse').iloc[0]['model']
best_saving_model_name = results_df.sort_values(by='saving_rmse').iloc[0]['model']

best_deposit_model = models[best_deposit_model_name]
best_saving_model = models[best_saving_model_name]

# 전체 데이터로 재학습 후 저장
best_deposit_model.fit(X, y_deposit)
best_saving_model.fit(X, y_saving)

joblib.dump(best_deposit_model, os.path.join(os.path.dirname(__file__), 'deposit_model.pkl'))
joblib.dump(best_saving_model, os.path.join(os.path.dirname(__file__), 'saving_model.pkl'))

print(f"\n✅ 저장 완료: deposit_model.pkl ({best_deposit_model_name}), saving_model.pkl ({best_saving_model_name})")
