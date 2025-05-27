<template>
  <div class="stock-preview">
    <!-- 헤더 -->
    <div class="preview-header">
      <div class="header-icon">
        <i class="fas fa-chart-trending-up"></i>
      </div>
      <div class="header-content">
        <h3>📊 오늘의 주식 요약</h3>
        <p class="header-subtitle">실시간 주식 시장 하이라이트</p>
      </div>
      <div class="live-indicator">
        <span class="pulse-dot"></span>
        <span class="live-text">LIVE</span>
      </div>
    </div>

    <!-- 로딩 상태 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">주식 데이터를 불러오고 있습니다...</p>
    </div>

    <!-- 메인 콘텐츠 -->
    <div v-else class="preview-content">
      <!-- ChatGPT AI 요약 -->
      <section v-if="data.ai_summary" class="ai-summary-section">
        <div class="section-header ai-header">
          <div class="ai-icon">
            <i class="fas fa-brain"></i>
          </div>
          <h4>🧠 ChatGPT 시장 분석</h4>
          <span class="ai-badge">AI 분석</span>
        </div>
        <div class="ai-content markdown-box" v-html="marked(data.ai_summary)"></div>
      </section>

      <!-- 주요 섹션들 -->
      <div class="sections-grid">
        <!-- 상승률 TOP 3 -->
        <section class="stock-section gainers-section">
          <div class="section-header">
            <div class="section-icon up-icon">
              <i class="fas fa-rocket"></i>
            </div>
            <h4>🚀 상승률 TOP 3</h4>
          </div>
          <div class="stock-items">
            <div 
              v-for="(item, index) in data.top_gainers.slice(0, 3)" 
              :key="item.종목명"
              class="stock-item up-item"
              :style="{ animationDelay: `${index * 0.1}s` }"
            >
              <div class="item-rank">{{ index + 1 }}</div>
              <div class="item-info">
                <h5 class="item-name">{{ item.종목명 }}</h5>
                <p class="item-price">{{ formatPrice(item.현재가) }}원</p>
              </div>
              <div class="item-change up">
                <span class="change-rate">+{{ item.등락률 }}%</span>
                <i class="fas fa-caret-up"></i>
              </div>
            </div>
          </div>
        </section>

        <!-- 하락률 TOP 3 -->
        <section class="stock-section losers-section">
          <div class="section-header">
            <div class="section-icon down-icon">
              <i class="fas fa-chart-line-down"></i>
            </div>
            <h4>📉 하락률 TOP 3</h4>
          </div>
          <div class="stock-items">
            <div 
              v-for="(item, index) in data.top_losers.slice(0, 3)" 
              :key="item.종목명"
              class="stock-item down-item"
              :style="{ animationDelay: `${index * 0.1}s` }"
            >
              <div class="item-rank">{{ index + 1 }}</div>
              <div class="item-info">
                <h5 class="item-name">{{ item.종목명 }}</h5>
                <p class="item-price">{{ formatPrice(item.현재가) }}원</p>
              </div>
              <div class="item-change down">
                <span class="change-rate">{{ item.등락률 }}%</span>
                <i class="fas fa-caret-down"></i>
              </div>
            </div>
          </div>
        </section>

        <!-- 시가총액 TOP 10 -->
        <section class="stock-section market-cap-section">
          <div class="section-header">
            <div class="section-icon cap-icon">
              <i class="fas fa-crown"></i>
            </div>
            <h4>💰 시가총액 TOP 10</h4>
          </div>
          <div class="market-cap-grid">
            <div 
              v-for="(item, index) in data.top30.slice(0, 10)" 
              :key="item.종목명"
              class="cap-item"
              :style="{ animationDelay: `${index * 0.05}s` }"
            >
              <div class="cap-rank">{{ index + 1 }}</div>
              <div class="cap-info">
                <h5 class="cap-name">{{ item.종목명 }}</h5>
                <p class="cap-price">{{ formatPrice(item.현재가) }}원</p>
                <p class="cap-market">{{ formatMarketCap(item.시가총액) }}</p>
              </div>
              <div class="cap-indicator" :class="getChangeClass(item.등락률)">
                <i class="fas" :class="getChangeIcon(item.등락률)"></i>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { marked } from 'marked'

const data = ref({
  top_gainers: [],
  top_losers: [],
  top30: [],
  ai_summary: ''
})
const loading = ref(true)

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

onMounted(async () => {
  try {
    const res = await axios.get(`${import.meta.env.VITE_API_URL}/videos/stock-summary/`)
    data.value = res.data
  } catch (err) {
    console.error('📉 주식요약 실패:', err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.stock-preview {
  background: linear-gradient(135deg, white);
  border-radius: 24px;
  padding: 28px;
  margin-top: 40px;
  box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
  position: relative;
  overflow: hidden;
}

.stock-preview::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
  backdrop-filter: blur(10px);
  z-index: 0;
}

.stock-preview > * {
  position: relative;
  z-index: 1;
}

/* 헤더 */
.preview-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.header-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
  box-shadow: 0 8px 20px rgba(255, 107, 107, 0.4);
}

.header-content {
  flex: 1;
}

.header-content h3 {
  font-size: 24px;
  font-weight: 800;
  color: black;
  margin: 0 0 4px 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.header-subtitle {
  font-size: 14px;
  color: black;
  margin: 0;
  font-weight: 500;
}

.live-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(34, 197, 94, 0.2);
  padding: 8px 16px;
  border-radius: 20px;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background: #22c55e;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.2); }
}

.live-text {
  font-size: 12px;
  color: #22c55e;
  font-weight: 700;
  letter-spacing: 0.5px;
}

/* 로딩 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  color: black;
  font-size: 16px;
  font-weight: 500;
}

/* 메인 콘텐츠 */
.preview-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* AI 요약 섹션 */
.ai-summary-section {
  background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%);
  border-radius: 20px;
  padding: 24px;
  border: 1px solid rgba(245, 158, 11, 0.3);
  box-shadow: 0 8px 32px rgba(245, 158, 11, 0.2);
  animation: fadeInUp 0.6s ease-out;
  max-height: 320px;             /* 원하는 최대 높이 */
  overflow-y: auto;              /* 내용 많으면 스크롤 */
  white-space: pre-wrap;         /* 줄바꿈 보존 */
}

.markdown-box {
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.6;
  font-size: 15px;
  color: #92400e;
  font-weight: 500;
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
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: white;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
}

.ai-header h4 {
  flex: 1;
  font-size: 18px;
  font-weight: 700;
  color: #92400e;
  margin: 0;
}

.ai-badge {
  background: rgba(245, 158, 11, 0.2);
  color: #92400e;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.ai-content p {
  font-size: 15px;
  color: #92400e;
  margin: 0;
  line-height: 1.6;
  font-weight: 500;
}

/* 섹션 그리드 */
.sections-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.market-cap-section {
  grid-column: 1 / -1;
}

/* 주식 섹션 */
.stock-section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 24px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
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
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.up-icon {
  background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
}

.down-icon {
  background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
}

.cap-icon {
  background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
}

.section-header h4 {
  font-size: 16px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

/* 주식 아이템들 */
.stock-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stock-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  animation: fadeInUp 0.6s ease-out both;
}

.stock-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.item-rank {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.item-info {
  flex: 1;
  min-width: 0;
}

.item-name {
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 4px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-price {
  font-size: 13px;
  color: #6b7280;
  margin: 0;
  font-weight: 500;
}

.item-change {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 700;
  padding: 6px 12px;
  border-radius: 10px;
}

.item-change.up {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  color: #dc2626;
}

.item-change.down {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  color: #2563eb;
}

/* 시가총액 그리드 */
.market-cap-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
}

.cap-item {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 12px;
  padding: 16px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  position: relative;
  animation: fadeInUp 0.6s ease-out both;
  text-align: center;
}

.cap-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.cap-rank {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 20px;
  height: 20px;
  background: linear-gradient(135deg, white 0%, #60a5fa 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 700;
  color: white;
}

.cap-info {
  padding-right: 24px;
}

.cap-name {
  font-size: 13px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
  line-height: 1.3;
}

.cap-price {
  font-size: 12px;
  color: #374151;
  margin: 0 0 4px 0;
  font-weight: 500;
}

.cap-market {
  font-size: 10px;
  color: #6b7280;
  margin: 0;
}

.cap-indicator {
  position: absolute;
  bottom: 8px;
  right: 8px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 8px;
}

.cap-indicator.up {
  background: #dc2626;
  color: white;
}

.cap-indicator.down {
  background: #2563eb;
  color: white;
}

.cap-indicator.neutral {
  background: #6b7280;
  color: white;
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
@media (max-width: 768px) {
  .stock-preview {
    padding: 20px;
    margin-top: 20px;
  }
  
  .preview-header {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }
  
  .sections-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .market-cap-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .header-content h3 {
    font-size: 20px;
  }
}

@media (max-width: 480px) {
  .market-cap-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .stock-section {
    padding: 16px;
  }
  
  .ai-summary-section {
    padding: 16px;
  }
}
</style>