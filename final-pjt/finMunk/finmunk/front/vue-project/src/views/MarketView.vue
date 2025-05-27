<template>
  <div class="products-view">
    <!-- 배너 -->
    <section class="banner">
      <div class="banner-content">
        <div class="banner-icon">💰</div>
        <h1>통화별 환율, 금리, 주요 금융지표를 한 눈에 확인하세요</h1>
        <p class="banner-date">{{ now }}</p>
      </div>
    </section>

    <!-- 로딩 애니메이션 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-container">
        <div class="loading-spinner">
          <div class="spinner"></div>
          <p>시장 데이터를 불러오는 중...</p>
        </div>
      </div>
    </div>

    <!-- 메인 컨텐츠 -->
    <main class="main-container" v-show="!isLoading">
      <ExchangeSummary :financial="financial" :dateLabel="dateLabel" />
      <CurrencyTable :rates="rates" @openCalculator="openCalculator" />
      <GoldTable />
      <NewsSection :news="news" />
    </main>

    <ExchangeCalculator 
      :isOpen="isCalculatorOpen" 
      :rates="simplifiedRates" 
      @close="closeCalculator" 
    />

    <Chatbot />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

import ExchangeSummary from '@/components/market/ExchangeSummary.vue'
import CurrencyTable from '@/components/market/CurrencyTable.vue'
import GoldTable from '@/components/market/GoldTable.vue'
import NewsSection from '@/components/market/NewsSection.vue'
import ExchangeCalculator from '@/components/market/Currencycalculator.vue'
import Chatbot from '@/components/chatbot/Chatbot.vue'

const API_URL = import.meta.env.VITE_API_URL
const now = ref('')
const rates = ref({})
const financial = ref({})
const news = ref([])
const dateLabel = ref('')
const isCalculatorOpen = ref(false)
const isLoading = ref(true)

const simplifiedRates = computed(() => {
  const r = rates.value
  return {
    USD: r.USD?.today ?? null,
    JPY: r.JPY?.today ?? null,
    EUR: r.EUR?.today ?? null,
    GBP: r.GBP?.today ?? null,
    CNY: r.CNY?.today ?? null,
    AUD: r.AUD?.today ?? null,
    CAD: r.CAD?.today ?? null,
    CHF: r.CHF?.today ?? null,
    HKD: r.HKD?.today ?? null,
  }
})

onMounted(async () => {
  try {
    // 로딩 애니메이션 (1.5초)
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    const res = await axios.get(`${API_URL}/market/summary`)
    rates.value = res.data.rates
    financial.value = res.data.financial_data
    news.value = res.data.news
    dateLabel.value = financial.value['기준일자'] ?? '기준일 없음'

    const nowTime = new Date()
    now.value = nowTime.toLocaleDateString('ko-KR', {
      year: 'numeric', month: '2-digit', day: '2-digit', weekday: 'long'
    }) + ' / 기준시간 ' + nowTime.toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
    
    isLoading.value = false
  } catch (error) {
    console.error('데이터 로딩 중 오류 발생:', error)
    isLoading.value = false
  }
})

function openCalculator() {
  isCalculatorOpen.value = true
}

function closeCalculator() {
  isCalculatorOpen.value = false
}
</script>

<style scoped>
/* 전체 레이아웃 */
.products-view {
  width: 100%;
  background: linear-gradient(135deg, #f8fffe 0%, #e8f5f2 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  position: relative;
}

/* 로딩 오버레이 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.loading-container {
  text-align: center;
  background: white;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(77, 208, 177, 0.2);
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4DD0B1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-spinner p {
  color: #666;
  font-size: 16px;
  font-weight: 500;
  margin: 0;
}

/* 배너 섹션 */
.banner {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #f0fdf4 100%);
  color: #1f2937;
  text-align: center;
  padding: 60px 20px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.banner::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="80" cy="40" r="1.5" fill="rgba(255,255,255,0.1)"/><circle cx="40" cy="80" r="1" fill="rgba(255,255,255,0.1)"/></svg>');
  animation: float 20s infinite linear;
}

@keyframes float {
  0% { transform: translateY(0px) rotate(0deg); }
  100% { transform: translateY(-100px) rotate(360deg); }
}

.banner-content {
  position: relative;
  z-index: 1;
  max-width: 800px;
}

.banner-icon {
  font-size: 48px;
  margin-bottom: 20px;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

.banner h1 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 15px;
  letter-spacing: -0.5px;
  line-height: 1.3;
}

.banner-date {
  font-size: 16px;
  opacity: 0.9;
  font-weight: 400;
  background: rgba(255, 255, 255, 0.2);
  padding: 10px 20px;
  border-radius: 25px;
  display: inline-block;
  backdrop-filter: blur(10px);
}

/* 메인 컨테이너 */
.main-container {
  width: 100%;
  max-width: 1200px;
  margin: -30px auto 0;
  padding: 0 20px 60px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
  position: relative;
  z-index: 2;
  animation: slideUp 0.8s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 컴포넌트 공통 스타일 개선 */
.main-container > * {
  width: 100%;
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(77, 208, 177, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.main-container > *::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #4DD0B1, #3CBFA0);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.main-container > *:hover {
  transform: translateY(-8px);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.12);
}

.main-container > *:hover::before {
  opacity: 1;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .banner {
    padding: 40px 15px;
  }
  
  .banner h1 {
    font-size: 24px;
  }
  
  .banner-icon {
    font-size: 36px;
  }
  
  .main-container {
    margin: -20px auto 0;
    padding: 0 15px 40px;
    gap: 20px;
  }
  
  .main-container > * {
    padding: 20px;
    border-radius: 16px;
  }
  
  .loading-container {
    padding: 30px 20px;
    margin: 0 15px;
  }
}

@media (max-width: 480px) {
  .banner {
    padding: 30px 10px;
  }
  
  .banner h1 {
    font-size: 20px;
  }
  
  .banner-date {
    font-size: 14px;
    padding: 8px 16px;
  }
  
  .main-container {
    margin: -15px auto 0;
    padding: 0 10px 30px;
  }
  
  .main-container > * {
    padding: 16px;
  }
}

/* 개별 컴포넌트 스타일링을 위한 deep selectors */
:deep(.exchange-summary) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

:deep(.currency-table) {
  background: white;
}

:deep(.gold-table) {
  background: white;
}

:deep(.news-section) {
  background: white;
}
</style>