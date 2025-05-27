<template>
  <div class="recommend-container" ref="root">
    <!-- 헤더 섹션 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-icon">💡</div>
        <div class="header-text">
          <h1 class="page-title">AI 금융상품 추천</h1>
          <p class="page-subtitle">당신만을 위한 맞춤형 금융 솔루션을 찾아보세요</p>
        </div>
      </div>
      <div class="header-decoration"></div>
    </div>

    <!-- 로딩 상태 -->
    <div v-if="!result && !error" class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">AI가 맞춤형 상품을 분석하고 있어요...</p>
    </div>

    <!-- 에러 상태 -->
    <div v-if="error" class="error-container">
      <div class="error-icon">😢</div>
      <h3>추천 정보를 불러오는 데 실패했어요</h3>
      <p>잠시 후 다시 시도해주세요</p>
      <button @click="retryRecommendation" class="retry-button">다시 시도</button>
    </div>

    <!-- 결과 표시 -->
    <div v-if="result && userInput" class="results-container">
      <!-- 예측 기준 카드 -->
      <div class="prediction-card">
        <div class="prediction-header">
          <div class="prediction-icon">📊</div>
          <div class="prediction-content">
            <h3 class="prediction-title">AI 분석 결과</h3>
            <p class="prediction-subtitle">회원님의 프로필을 기반으로 한 최적 투자 기준</p>
          </div>
        </div>

        <div class="prediction-results">
          <div class="prediction-item deposit" @click="scrollTo('deposit')">
            <div class="prediction-type">
              <span class="type-icon">🏛️</span>
              <span class="type-name">예금</span>
            </div>
            <div class="prediction-details">
              <span class="detail-label">추천 기간</span>
              <span class="detail-value">{{ result.predicted_deposit.months }}개월</span>
            </div>
            <div class="prediction-details">
              <span class="detail-label">추천 금액</span>
              <span class="detail-value highlight">{{ result.predicted_deposit.amount }}만원</span>
            </div>
            <div class="click-hint">클릭하여 예금 추천 보기 👆</div>
          </div>

          <div class="prediction-item saving" @click="scrollTo('saving')">
            <div class="prediction-type">
              <span class="type-icon">💰</span>
              <span class="type-name">적금</span>
            </div>
            <div class="prediction-details">
              <span class="detail-label">추천 기간</span>
              <span class="detail-value">{{ result.predicted_saving.months }}개월</span>
            </div>
            <div class="prediction-details">
              <span class="detail-label">추천 금액</span>
              <span class="detail-value highlight">{{ result.predicted_saving.amount }}만원</span>
            </div>
            <div class="click-hint">클릭하여 적금 추천 보기 👆</div>
          </div>
        </div>
      </div>

      <!-- 추천 상품 카드들 -->
      <div class="recommendations-section">
        <div id="deposit-section">
          <RecommendResultCard
            ref="depositSection"
            title="예금"
            :products="result.recommended_deposit"
            :user="userInput"
          />
        </div>
        <div id="saving-section">
          <RecommendResultCard
            ref="savingSection"
            title="적금"
            :products="result.recommended_saving"
            :user="userInput"
          />
        </div>
      </div>
    </div>
  </div>
  <Chatbot/>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'
import RecommendResultCard from '@/components/recommend/Recommendresultcard.vue'
import Chatbot from '@/components/chatbot/Chatbot.vue'

const API_URL = import.meta.env.VITE_API_URL
const result = ref(null)
const userInput = ref(null)
const error = ref(false)

const depositSection = ref(null)
const savingSection = ref(null)

// 개선된 스크롤 함수
const scrollTo = (type) => {
  nextTick(() => {
    let targetElement = null
    
    if (type === 'deposit') {
      // 1. ID로 찾기 (가장 확실한 방법)
      targetElement = document.getElementById('deposit-section')
      
      // 2. ref로 찾기 (백업 방법)
      if (!targetElement && depositSection.value) {
        if (depositSection.value.$el) {
          targetElement = depositSection.value.$el
        } else if (depositSection.value.root) {
          targetElement = depositSection.value.root
        }
      }
    } else if (type === 'saving') {
      // 1. ID로 찾기 (가장 확실한 방법)
      targetElement = document.getElementById('saving-section')
      
      // 2. ref로 찾기 (백업 방법)
      if (!targetElement && savingSection.value) {
        if (savingSection.value.$el) {
          targetElement = savingSection.value.$el
        } else if (savingSection.value.root) {
          targetElement = savingSection.value.root
        }
      }
    }
    
    if (targetElement) {
      targetElement.scrollIntoView({ 
        behavior: 'smooth',
        block: 'start',
        inline: 'nearest'
      })
      
      // 스크롤 후 약간의 애니메이션 효과
      targetElement.style.transform = 'scale(1.02)'
      targetElement.style.transition = 'transform 0.3s ease'
      
      setTimeout(() => {
        targetElement.style.transform = 'scale(1)'
      }, 300)
    } else {
      console.warn(`${type} 섹션을 찾을 수 없습니다.`)
    }
  })
}

const fetchRecommendations = async () => {
  try {
    error.value = false

    const profileRes = await axios.get(`${API_URL}/users/profile/`, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })

    userInput.value = {
      age: profileRes.data.age,
      job: profileRes.data.job ? 1 : 0,
      monthly_income: profileRes.data.income,
      assets: profileRes.data.assets
    }

    const recommendRes = await axios.post(`${API_URL}/products/recommend/`, {}, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })

    result.value = recommendRes.data
  } catch (err) {
    console.error('추천 실패:', err)
    error.value = true
  }
}

const retryRecommendation = () => {
  result.value = null
  fetchRecommendations()
}

onMounted(() => {
  fetchRecommendations()
})

const root = ref(null)

defineExpose({ root }) 
</script>

<style scoped>
.recommend-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #f0fdf4 100%);
}

.page-header {
  text-align: center;
  margin-bottom: 48px;
  position: relative;
  padding: 40px 0;
  animation: fadeInDown 0.8s ease-out;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

.header-icon {
  font-size: 48px;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

.header-text {
  text-align: left;
}

.page-title {
  font-size: 36px;
  font-weight: 800;
  background: linear-gradient(135deg, #1e40af 0%, #10b981 50%, #059669 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0 0 8px 0;
  letter-spacing: -0.025em;
}

.page-subtitle {
  font-size: 16px;
  color: #6b7280;
  margin: 0;
  font-weight: 500;
}

.header-decoration {
  width: 100px;
  height: 4px;
  background: linear-gradient(90deg, #10b981, #34d399, #6ee7b7);
  margin: 0 auto;
  border-radius: 2px;
  animation: scaleIn 1s ease-out 0.5s both;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes scaleIn {
  from {
    transform: scaleX(0);
  }
  to {
    transform: scaleX(1);
  }
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  animation: fadeIn 0.6s ease-out;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #e5e7eb;
  border-top: 4px solid #10b981;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  font-size: 16px;
  color: #6b7280;
  font-weight: 500;
}

.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
  animation: fadeIn 0.6s ease-out;
}

.error-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.error-container h3 {
  font-size: 24px;
  font-weight: 700;
  color: #374151;
  margin: 0 0 8px 0;
}

.error-container p {
  font-size: 16px;
  color: #6b7280;
  margin: 0 0 24px 0;
}

.retry-button {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
}

.retry-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.4);
}

.results-container {
  animation: fadeInUp 0.8s ease-out;
}

.prediction-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border-radius: 24px;
  padding: 32px;
  margin-bottom: 32px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.prediction-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.12);
}

.prediction-header {
  display: flex;
  align-items: center;
  margin-bottom: 28px;
  padding-bottom: 20px;
  border-bottom: 2px solid rgba(59, 130, 246, 0.1);
}

.prediction-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  font-size: 24px;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
}

.prediction-content {
  flex: 1;
}

.prediction-title {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 4px 0;
  letter-spacing: -0.025em;
}

.prediction-subtitle {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
  font-weight: 500;
}

.prediction-results {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.prediction-item {
  background: linear-gradient(135deg, #fafafa 0%, #ffffff 100%);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
}

.prediction-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.prediction-item:active {
  transform: translateY(0);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.prediction-item.deposit {
  border-left: 4px solid #3b82f6;
}

.prediction-item.saving {
  border-left: 4px solid #10b981;
}

.prediction-type {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.type-icon {
  font-size: 24px;
  margin-right: 12px;
}

.type-name {
  font-size: 18px;
  font-weight: 700;
  color: #374151;
}

.prediction-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.detail-label {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

.detail-value {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
}

.detail-value.highlight {
  color: #1d4ed8;
  font-weight: 700;
}

.click-hint {
  font-size: 12px;
  color: #9ca3af;
  text-align: center;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  font-weight: 500;
}

.recommendations-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

#deposit-section,
#saving-section {
  scroll-margin-top: 80px; /* 스크롤 시 상단 여백 */
  transition: transform 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .recommend-container {
    padding: 16px;
  }
  
  .page-header {
    padding: 20px 0;
    margin-bottom: 32px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 16px;
  }
  
  .header-text {
    text-align: center;
  }
  
  .page-title {
    font-size: 28px;
  }
  
  .prediction-card {
    padding: 20px;
  }
  
  .prediction-results {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .prediction-item {
    padding: 20px;
  }
  
  #deposit-section,
  #saving-section {
    scroll-margin-top: 60px;
  }
}
</style>