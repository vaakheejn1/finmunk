<template>
    <div class="video-view">
      <!-- 헤더 섹션 -->
      <div class="page-header">
        <div class="header-content">
          <div class="header-icon">🎬</div>
          <div class="header-text">
            <h1 class="page-title">비디오 & 주식 정보</h1>
            <p class="page-subtitle">영상 검색부터 주식 시장 분석까지 한 번에</p>
          </div>
        </div>
        <div class="header-decoration"></div>
      </div>
  
      <!-- 탭 네비게이션 -->
      <div class="tab-navigation">
        <button 
          @click="currentView = 'search'" 
          :class="{ active: currentView === 'search' }"
          class="tab-btn"
        >
          <i class="fas fa-search"></i>
          <span>영상 검색</span>
        </button>
        <button 
          @click="currentView = 'saved'" 
          :class="{ active: currentView === 'saved' }"
          class="tab-btn"
        >
          <i class="fas fa-bookmark"></i>
          <span>저장된 영상</span>
        </button>
        <button 
          @click="currentView = 'stocks'" 
          :class="{ active: currentView === 'stocks' }"
          class="tab-btn"
        >
          <i class="fas fa-chart-line"></i>
          <span>주식 시장</span>
        </button>
      </div>
  
      <!-- 메인 콘텐츠 영역 -->
      <div class="main-content">
        <component :is="viewComponent" />
      </div>
  
      <!-- 주식 요약 프리뷰 (주식 탭이 아닐 때만 표시) -->
      <div v-if="currentView !== 'stocks'" class="stock-preview-section">
        <StockSummaryPreview />
      </div>
    </div>
    <Chatbot/>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  
  import VideoSearch from '@/components/video/VideoSearch.vue'
  import VideoSaved from '@/components/video/VideoSaved.vue'
  import StockSummary from '@/components/video/StockSummary.vue'
  import StockSummaryPreview from '@/components/video/StockSummaryPreview.vue'
    import Chatbot from '@/components/chatbot/Chatbot.vue'
  
  const currentView = ref('search')
  
  const viewComponent = computed(() => {
    if (currentView.value === 'search') return VideoSearch
    if (currentView.value === 'saved') return VideoSaved
    if (currentView.value === 'stocks') return StockSummary
    return null
  })
  </script>
  
  <style scoped>
  .video-view {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    min-height: 100vh;
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #f0fdf4 100%);
  }
  
  /* 헤더 섹션 */
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
  
  /* 탭 네비게이션 */
  .tab-navigation {
    display: flex;
    gap: 16px;
    margin-bottom: 32px;
    padding: 0 4px;
    justify-content: center;
  }
  
  .tab-btn {
    flex: 1;
    max-width: 200px;
    padding: 16px 24px;
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border: 2px solid rgba(59, 130, 246, 0.1);
    border-radius: 16px;
    color: #6b7280;
    font-weight: 600;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    backdrop-filter: blur(10px);
  }
  
  .tab-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    border-color: rgba(59, 130, 246, 0.3);
  }
  
  .tab-btn.active {
    background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
    color: white;
    border-color: #3b82f6;
    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
  }
  
  .tab-btn i {
    font-size: 18px;
  }
  
  /* 메인 콘텐츠 */
  .main-content {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 32px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    animation: fadeInUp 0.6s ease-out;
  }
  
  .main-content:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
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
  
  /* 주식 프리뷰 섹션 */
  .stock-preview-section {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    animation: fadeInUp 0.6s ease-out 0.2s both;
  }
  
  .stock-preview-section:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
  }
  
  /* 반응형 디자인 */
  @media (max-width: 768px) {
    .video-view {
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
    
    .tab-navigation {
      flex-direction: column;
      gap: 12px;
    }
    
    .tab-btn {
      max-width: none;
      padding: 12px 16px;
      font-size: 14px;
    }
    
    .main-content,
    .stock-preview-section {
      padding: 24px;
    }
  }
  
  @media (max-width: 480px) {
    .video-view {
      padding: 12px;
    }
    
    .header-icon {
      font-size: 40px;
    }
    
    .page-title {
      font-size: 24px;
    }
    
    .page-subtitle {
      font-size: 14px;
    }
    
    .tab-btn {
      padding: 10px 12px;
      font-size: 13px;
    }
    
    .main-content,
    .stock-preview-section {
      padding: 20px;
    }
  }
  </style>