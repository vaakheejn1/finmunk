<template>
  <div class="stock-summary">
    <!-- 주식 헤더 -->
    <div class="stock-header">
      <div class="stock-icon">
        <i class="fas fa-chart-line"></i>
      </div>
      <div class="stock-title">
        <h3>주식 시장 분석</h3>
        <p>실시간 주식 시장 동향과 AI 분석을 확인하세요</p>
      </div>
      <div class="market-status">
        <span class="status-indicator"></span>
        <span class="status-text">시장 개장</span>
      </div>
    </div>

    <!-- AI 요약 카드 -->
    <div v-if="stockData.ai_summary" class="ai-summary-card">
      <div class="ai-header">
        <div class="ai-icon">
          <i class="fas fa-brain"></i>
        </div>
        <div class="ai-title">
          <h4>🧠 ChatGPT 시장 분석</h4>
          <span class="ai-badge">AI 분석</span>
        </div>
      </div>

      <!-- ✅ 줄바꿈 + 마크다운 반영 -->
      <div class="ai-content markdown-box" v-html="marked(stockData.ai_summary)"></div>
    </div>

    <!-- 주식 섹션들 -->
    <div class="stock-sections">
      <!-- 상승률 TOP 10 -->
      <div class="stock-section gainers">
        <div class="section-header">
          <div class="section-icon up">
            <i class="fas fa-trending-up"></i>
          </div>
          <div class="section-title">
            <h4>🚀 상승률 TOP 10</h4>
            <p>오늘 가장 많이 오른 종목들</p>
          </div>
        </div>
        
        <div class="stock-list">
          <div 
            v-for="(item, index) in stockData.top_gainers" 
            :key="item.종목명"
            class="stock-item"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <div class="stock-rank">{{ index + 1 }}</div>
            <div class="stock-info">
              <h5 class="stock-name">{{ item.종목명 }}</h5>
              <p class="stock-price">{{ formatPrice(item.현재가) }}원</p>
            </div>
            <div class="stock-change up">
              <span class="change-rate">+{{ item.등락률 }}%</span>
              <i class="fas fa-caret-up"></i>
            </div>
          </div>
        </div>
      </div>

      <!-- 하락률 TOP 10 -->
      <div class="stock-section losers">
        <div class="section-header">
          <div class="section-icon down">
            <i class="fas fa-trending-down"></i>
          </div>
          <div class="section-title">
            <h4>📉 하락률 TOP 10</h4>
            <p>오늘 가장 많이 내린 종목들</p>
          </div>
        </div>
        
        <div class="stock-list">
          <div 
            v-for="(item, index) in stockData.top_losers" 
            :key="item.종목명"
            class="stock-item"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <div class="stock-rank">{{ index + 1 }}</div>
            <div class="stock-info">
              <h5 class="stock-name">{{ item.종목명 }}</h5>
              <p class="stock-price">{{ formatPrice(item.현재가) }}원</p>
            </div>
            <div class="stock-change down">
              <span class="change-rate">{{ item.등락률 }}%</span>
              <i class="fas fa-caret-down"></i>
            </div>
          </div>
        </div>
      </div>

      <!-- 시가총액 TOP 30 -->
      <div class="stock-section market-cap">
        <div class="section-header">
          <div class="section-icon cap">
            <i class="fas fa-crown"></i>
          </div>
          <div class="section-title">
            <h4>💰 시가총액 TOP 30</h4>
            <p>대한민국 대표 대기업들</p>
          </div>
        </div>
        
        <div class="stock-grid">
          <div 
            v-for="(item, index) in stockData.top30" 
            :key="item.종목명"
            class="stock-card"
            :style="{ animationDelay: `${index * 0.05}s` }"
          >
            <div class="card-rank">{{ index + 1 }}</div>
            <div class="card-content">
              <h5 class="card-name">{{ item.종목명 }}</h5>
              <p class="card-price">{{ formatPrice(item.현재가) }}원</p>
              <p class="card-cap">시총: {{ formatMarketCap(item.시가총액) }}</p>
            </div>
            <div class="card-indicator" :class="getChangeClass(item.등락률)">
              <i class="fas" :class="getChangeIcon(item.등락률)"></i>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 로딩 상태 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">주식 데이터를 불러오고 있어요...</p>
    </div>

    <!-- 에러 상태 -->
    <div v-if="error" class="error-container">
      <div class="error-icon">📊</div>
      <h3>데이터를 불러올 수 없어요</h3>
      <p>잠시 후 다시 시도해주세요</p>
      <button @click="fetchStockData" class="retry-btn">
        <i class="fas fa-redo"></i>
        다시 시도
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import {marked} from 'marked'

const stockData = ref({
  top_gainers: [],
  top_losers: [],
  top30: [],
  ai_summary: ''
})

const loading = ref(false)
const error = ref(false)

const fetchStockData = async () => {
  loading.value = true
  error.value = false
  
  try {
    const res = await axios.get(`${import.meta.env.VITE_API_URL}/videos/stock-summary/`)
    stockData.value = res.data
  } catch (err) {
    console.error('📉 주식 데이터 로드 실패:', err)
    error.value = true
  } finally {
    loading.value = false
  }
}

const formatPrice = (price) => {
  return parseInt(price).toLocaleString()
}

const formatMarketCap = (cap) => {
  const num = parseInt(cap)
  if (num >= 1000000000000) {
    return `${(num / 1000000000000).toFixed(1)}조원`
  } else if (num >= 100000000) {
    return `${(num / 100000000).toFixed(0)}억원`
  }
  return `${num.toLocaleString()}원`
}

const getChangeClass = (rate) => {
  const num = parseFloat(rate)
  if (num > 0) return 'up'
  if (num < 0) return 'down'
  return 'neutral'
}

const getChangeIcon = (rate) => {
  const num = parseFloat(rate)
  if (num > 0) return 'fa-caret-up'
  if (num < 0) return 'fa-caret-down'
  return 'fa-minus'
}

onMounted(() => {
  fetchStockData()
})
</script>

<style scoped>
.stock-summary {
  max-width: 1200px;
  margin: 0 auto;
}

/* 주식 헤더 */
.stock-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
  padding-bottom: 20px;
  border-bottom: 2px solid rgba(59, 130, 246, 0.1);
}

.stock-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: white;
  box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
}

.stock-title {
  flex: 1;
}

.stock-title h3 {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 4px 0;
}

.stock-title p {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.market-status {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
  padding: 8px 16px;
  border-radius: 20px;
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.status-indicator {
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.status-text {
  font-size: 12px;
  color: #059669;
  font-weight: 600;
}

/* AI 요약 카드 */
.ai-summary-card {
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
  border: 1px solid rgba(245, 158, 11, 0.2);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 32px;
  box-shadow: 0 4px 16px rgba(245, 158, 11, 0.1);
  animation: fadeInUp 0.6s ease-out;
  max-height: 280px;       
  overflow-y: auto;        
  white-space: pre-wrap;   
}

.ai-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.ai-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  color: white;
}

.ai-title h4 {
  font-size: 16px;
  font-weight: 700;
  color: #92400e;
  margin: 0;
}

.ai-badge {
  background: rgba(245, 158, 11, 0.2);
  color: #92400e;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.ai-content p {
  font-size: 14px;
  color: #92400e;
  margin: 0;
  line-height: 1.6;
  font-weight: 500;
}

/* 주식 섹션들 */
.stock-sections {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.stock-section {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  animation: fadeInUp 0.6s ease-out;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.section-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  color: white;
}

.section-icon.up {
  background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
}

.section-icon.down {
  background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
}

.section-icon.cap {
  background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
}

.section-title h4 {
  font-size: 16px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.section-title p {
  font-size: 12px;
  color: #6b7280;
  margin: 0;
}

/* 주식 리스트 - 5개씩 그리드로 변경 */
.stock-list {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

.stock-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px 12px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  animation: fadeInUp 0.6s ease-out both;
  text-align: center;
}

.stock-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  border-color: rgba(59, 130, 246, 0.2);
}

.stock-rank {
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
  margin-bottom: 4px;
}

.stock-info {
  flex: 1;
  min-width: 0;
  margin-bottom: 8px;
}

.stock-name {
  font-size: 13px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 4px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-align: center;
}

.stock-price {
  font-size: 11px;
  color: #6b7280;
  margin: 0;
  text-align: center;
}

.stock-change {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 8px;
}

.stock-change.up {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  color: #dc2626;
}

.stock-change.down {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  color: #2563eb;
}

.change-rate {
  font-weight: 700;
}

/* 주식 그리드 (시가총액용) - 5개씩 고정 */
.stock-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

.stock-card {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 12px;
  padding: 16px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  position: relative;
  animation: fadeInUp 0.6s ease-out both;
}

.stock-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1);
  border-color: rgba(59, 130, 246, 0.2);
}

.card-rank {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 24px;
  height: 24px;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 700;
  color: white;
}

.card-content {
  padding-right: 32px;
}

.card-name {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
  line-height: 1.3;
}

.card-price {
  font-size: 13px;
  color: #374151;
  margin: 0 0 4px 0;
  font-weight: 500;
}

.card-cap {
  font-size: 11px;
  color: #6b7280;
  margin: 0;
}

.card-indicator {
  position: absolute;
  bottom: 8px;
  right: 8px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 8px;
}

.card-indicator.up {
  background: #dc2626;
  color: white;
}

.card-indicator.down {
  background: #2563eb;
  color: white;
}

.card-indicator.neutral {
  background: #6b7280;
  color: white;
}

/* 로딩 상태 */
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

/* 에러 상태 */
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

.retry-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
}

.retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 반응형 디자인 */
@media (max-width: 1200px) {
  .stock-list,
  .stock-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 900px) {
  .stock-list,
  .stock-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .stock-header {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }
  
  .stock-sections {
    gap: 24px;
  }
  
  .stock-section {
    padding: 20px;
  }
  
  .stock-list,
  .stock-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .stock-item {
    padding: 12px 8px;
  }
  
  .stock-card {
    padding: 12px;
  }
}

@media (max-width: 480px) {
  .stock-list,
  .stock-grid {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .ai-summary-card::-webkit-scrollbar {
  width: 6px;
  }
  .ai-summary-card::-webkit-scrollbar-thumb {
    background-color: rgba(245, 158, 11, 0.3);
    border-radius: 4px;
  }
  
  .ai-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .markdown-box {
  white-space: pre-wrap;
  line-height: 1.6;
  color: #92400e;
  font-size: 14px;
  font-weight: 500;
  }
}
</style>