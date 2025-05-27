<template>
  <div class="homepage-wrapper">
    <!-- 메인 슬라이드 섹션 -->
    <section class="hero-section">
      <div class="carousel-container">
        <div class="carousel-track" :style="{ transform: `translateX(-${currentSlide * 100}%)` }">
          <div :class="['slide', slide.bgClass]" v-for="(slide, index) in slides" :key="index">
            <div class="slide-overlay"></div>
            <div class="slide-content">
              <div class="content-wrapper">
                <h1 class="slide-title">{{ slide.title }}</h1>
                <p class="slide-description">{{ slide.description }}</p>

              </div>
              <div class="slide-image">
                <img :src="slide.image" :alt="slide.alt" />
                <div class="image-glow"></div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 슬라이드 컨트롤 -->
        <div class="carousel-controls">
          <div class="carousel-dots">
            <button 
              v-for="(slide, index) in slides" 
              :key="index"
              :class="['dot', { active: currentSlide === index }]"
              @click="goToSlide(index)"
            ></button>
          </div>
          <div class="carousel-nav">
            <button @click="prevSlide" class="nav-btn prev">‹</button>
            <button @click="nextSlide" class="nav-btn next">›</button>
          </div>
        </div>
      </div>
    </section>

    <!-- 메인 콘텐츠 -->
    <main class="main-content">
      <!-- FINMUNK 소개 섹션 -->
      <section class="intro-section">
        <div class="container">
          <div class="section-header">
            <h2 class="section-title">FINMUNK란?</h2>
            <p class="section-subtitle">혁신적인 금융 플랫폼으로 여러분의 금융생활을 더 스마트하게</p>
          </div>
          
          <div class="intro-grid">
            <div class="intro-card" v-for="(feature, index) in features" 
                 :key="index" 
                 :style="{ animationDelay: `${index * 0.2}s` }"
                 @click="handleIntroClick(feature.title)"
                 >
                 
              <div class="card-icon">
                <i :class="feature.icon"></i>
              </div>
              <h3 class="card-title">{{ feature.title }}</h3>
              <p class="card-description">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 람쥐 캐릭터 소개 -->
      <section class="character-section">
        <div class="container">
          <div class="character-content">
            <div class="character-info">
              <h2 class="section-title">만나보세요, 람쥐! 🐿️</h2>
              <p class="character-description">
                FINMUNK의 귀여운 마스코트 람쥐가 여러분의 금융 여정을 함께 합니다. 
                복잡한 금융 상품도 람쥐와 함께라면 쉽고 재미있게!
              </p>
              <div class="character-features">
                <div class="feature-item">
                  <span class="feature-icon">💡</span>
                  <span>똑똑한 금융 조언</span>
                </div>
                <div class="feature-item">
                  <span class="feature-icon">🎯</span>
                  <span>맞춤형 상품 추천</span>
                </div>
                <div class="feature-item">
                  <span class="feature-icon">🤝</span>
                  <span>24시간 상담 지원</span>
                </div>
              </div>
            </div>
            <div class="character-visual">
              <div class="character-circle">
                <img :src="daramglass" alt="람쥐 캐릭터" class="character-image" />
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 서비스 그리드 -->
      <section class="services-section">
        <div class="container">
          <div class="services-grid">
            <!-- 커뮤니티 -->
            <div class="service-card community" @click="handleServiceClick('community')">
              <div class="card-background">
                <div class="bg-pattern"></div>
                <div class="floating-shapes">
                  <div class="shape shape-1"></div>
                  <div class="shape shape-2"></div>
                  <div class="shape shape-3"></div>
                </div>
              </div>
              <div class="card-content">
                <div class="service-icon">
                  <i class="fas fa-users"></i>
                </div>
                <h3 class="service-title">커뮤니티</h3>
                <p class="service-description">오늘의 금융이야기를 확인해보세요!</p>
                <div class="service-stats">
                </div>
                <div class="service-arrow">
                  <i class="fas fa-arrow-right"></i>
                </div>
              </div>
            </div>

            <!-- 재테크 정보 -->
            <div class="service-card finance" @click="handleServiceClick('finance-info')">
              <div class="card-background">
                <div class="bg-pattern"></div>
                <div class="floating-shapes">
                  <div class="shape shape-1"></div>
                  <div class="shape shape-2"></div>
                  <div class="shape shape-3"></div>
                </div>
              </div>
              <div class="card-content">
                <div class="service-icon">
                  <i class="fas fa-chart-line"></i>
                </div>
                <h3 class="service-title">재테크 정보</h3>
                <p class="service-description">모닝브리핑</p>
                <div class="service-badge">
                </div>
                <div class="service-arrow">
                  <i class="fas fa-arrow-right"></i>
                </div>
              </div>
            </div>

            <!-- 은행 찾기 -->
            <div class="service-card bank" @click="handleServiceClick('bank-finder')">
              <div class="card-background">
                <div class="bg-pattern"></div>
                <div class="floating-shapes">
                  <div class="shape shape-1"></div>
                  <div class="shape shape-2"></div>
                  <div class="shape shape-3"></div>
                </div>
              </div>
              <div class="card-content">
                <div class="service-icon">
                  <i class="fas fa-map-marker-alt"></i>
                </div>
                <h3 class="service-title">내 주변 은행 찾기</h3>
                <p class="service-description">내 주변 은행을 간편하게 찾아보세요</p>
                <div class="service-arrow">
                  <i class="fas fa-arrow-right"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 하단 정보 섹션 -->
      <section class="bottom-info-section">
        <div class="container">
          <div class="info-grid">
            <!-- 공지사항 -->
            <div class="info-panel">
              <div class="panel-header">
                <h3 class="panel-title">
                  <i class="fas fa-bullhorn"></i>
                  공지사항
                </h3>
              </div>
                    <ul class="notice-list">
                    <li 
                    v-for="notice in notices" 
                    :key="notice.id" 
                    class="notice-item"
                    @click="goToArticle(notice.id)"
                    >
                    <span class="notice-title">{{ notice.title }}</span>
                    <span class="notice-date">{{ notice.date }}</span>
                    </li>
                    </ul>
            </div>

            <!-- 커뮤니티 인기글 -->
            <div class="info-panel">
              <div class="panel-header">
                <h3 class="panel-title">
                  <i class="fas fa-fire"></i>
                  커뮤니티 인기글
                </h3>
              </div>
              <ul class="popular-list">
                <li 
                  v-for="post in popularPosts" 
                  :key="post.id" 
                  class="popular-item"
                  @click="goToArticle(post.id)"
                >
                  <div class="post-info">
                    <span class="post-title">{{ post.title }}</span>
                    <div class="post-meta">
                      <span class="post-likes">❤️ {{ post.likes }}</span>
                      <span class="post-comments">💬 {{ post.comments }}</span>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>
    </main>

  </div>
  <div
  class="slide"
  v-for="(slide, index) in slides"
  :key="index"
  :class="slide.bgClass"
></div>
<Chatbot ref="chatbotRef" />
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import daramHelpLogo from '@/assets/daramhelplogo.png'
import daramglass from '@/assets/daramglass.png'
import daramsmart from '@/assets/daramsmart.png'
import daramai from '@/assets/daramai.png'
import daramtrip from '@/assets/daramtrip.png'
import Chatbot from '@/components/chatbot/Chatbot.vue'
import { useRouter } from 'vue-router'
import axios from 'axios'


const chatbotRef = ref(null)


const router = useRouter()

// 슬라이드 데이터
const slides = ref([
  {
    title: '스마트한 금융생활의 시작',
    description: 'FINMUNK와 함께 더 나은 금융 미래를 설계하세요',
    image: daramsmart,
    alt: '람쥐 스마트',
    action: 'get-started',
    bgClass: 'slide-bg-blue'
  },
  {
    title: '람쥐와 함께하는 금융여행',
    description: '귀여운 람쥐가 당신의 금융 파트너가 되어드립니다',
    image: daramHelpLogo,
    alt: '람쥐 파트너',
    action: 'recommend',
    bgClass: 'slide-bg-green'
  },
  {
    title: 'AI 기반 맞춤형 추천',
    description: '당신만을 위한 최적의 금융상품을 찾아드립니다',
    image: daramai,
    alt: '람쥐 AI',
    action: 'compare',
    bgClass: 'slide-bg-purple'
  },
  {
    title: '여행도 금융도 즐겁게!',
    description: '람쥐와 함께하는 즐거운 금융 여행을 시작해보세요',
    image: daramtrip,
    alt: '람쥐 여행',
    action: 'learn-more',
    bgClass: 'slide-bg-pink'
  }
])

const currentSlide = ref(0)
let slideTimer = null

// FINMUNK 특징
const features = ref([
  {
    icon: 'fas fa-robot',
    title: 'AI 기반 추천',
    description: '개인 맞춤형 금융상품을 AI가 분석하여 추천해드립니다'
  },
  {
    icon: 'fas fa-shield-alt',
    title: '실시간 시세',
    description: '실시간 금융시세 제공으로 발빠른 금융거래를 보장합니다'
  },
  {
    icon: 'fas fa-chart-pie',
    title: '통합 관리',
    description: '모든 금융 정보를 한 곳에서 편리하게 관리하세요'
  },
  {
    icon: 'fas fa-headset',
    title: '24시간 지원',
    description: '언제든지 궁금한 것이 있으면 람쥐봇이 도와드립니다'
  }
])


// intro - grid
function handleIntroClick(title) {
  if (title === 'AI 기반 추천') {
    router.push({ name: 'Recommend' })
  } else if (title === '실시간 시세') {
    router.push({ name: 'Market' })
  } else if (title === '통합 관리') {
    router.push({ name: 'MyPage' })
  } else if (title === '24시간 지원') {
    // 람쥐봇 자동 오픈
    if (chatbotRef.value && typeof chatbotRef.value.openChatbot === 'function') {
      chatbotRef.value.openChatbot()
    } else {
      alert('람쥐봇을 찾을 수 없어요 🐿️')
    }
  }
}



// 공지사항

const notices = ref([])
function loadNotices() {
  axios.get(`${import.meta.env.VITE_API_URL}/community/articles/?category=notice`)
    .then(res => {
      notices.value = res.data.map(n => ({
        id: n.id,
        title: n.title,
        date: n.created_at.split('T')[0]  // "2025-05-12T..." → "2025-05-12"
      }))
    })
    .catch(err => {
      console.error('공지사항 로딩 실패:', err)
    })
}

onMounted(() => {
  loadNotices()
  loadPopularPosts()
})



function goToArticle(articleId) {
  router.push({ name: 'CommunityArticle', params: { id: articleId } })
}


// 커뮤니티 인기글
const popularPosts = ref([])

function loadPopularPosts() {
  axios.get(`${import.meta.env.VITE_API_URL}/community/articles/popular/`)
    .then(res => {
      popularPosts.value = res.data.map(post => ({
        id: post.id,
        title: post.title,
        likes: post.like_count,
        comments: post.comment_count,
      }))
    })
    .catch(err => {
      console.error('인기글 불러오기 실패:', err)
    })
}

// 슬라이드 함수들
function goToSlide(index) {
  currentSlide.value = index
  resetSlideTimer()
}

function nextSlide() {
  currentSlide.value = (currentSlide.value + 1) % slides.value.length
}

function prevSlide() {
  currentSlide.value = currentSlide.value === 0 ? slides.value.length - 1 : currentSlide.value - 1
  resetSlideTimer()
}

function resetSlideTimer() {
  if (slideTimer) {
    clearInterval(slideTimer)
  }
  slideTimer = setInterval(nextSlide, 10000) // 10초 간격
}

// 이벤트 핸들러들
function handleSlideAction(action) {
  console.log(`슬라이드 액션: ${action}`)
  // 라우터로 페이지 이동 로직 추가
}

function handleServiceClick(service) {
  if (service === 'community') {
    router.push({ name: 'Community' })
  } else if (service === 'finance-info') {
    router.push({ name: 'Market' }) // MarketView.vue에 대응
  } else if (service === 'bank-finder') {
    router.push({ name: 'Bankmap' }) // BankMapView.vue에 대응
  } else {
    console.warn('알 수 없는 서비스:', service)
  }
}
// 라이프사이클
onMounted(() => {
  resetSlideTimer()
})

onUnmounted(() => {
  if (slideTimer) {
    clearInterval(slideTimer)
  }
})
</script>

<style scoped>
.homepage-wrapper {
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #f0fdf4 100%);
  min-height: 100vh;
}


.intro-card {
  cursor: pointer;
}

/* 히어로 섹션 */
.hero-section {
  position: relative;
  height: 50vh;
  overflow: hidden;
  min-height: 400px;
}

.carousel-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.carousel-track {
  display: flex;
  height: 100%;
  transition: transform 1s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide {
  flex: 0 0 100%;
  position: relative;
  display: flex;
  align-items: center;
  overflow: hidden;
}

.slide-bg-blue {
  background: linear-gradient(-135deg, #dbeafe, #93c5fd); /* 연하늘 */
}
.slide-bg-green {
  background: linear-gradient(-135deg, #d1fae5, #6ee7b7); /* 연초록 */
}
.slide-bg-purple {
  background: linear-gradient(-135deg, #ede9fe, #c4b5fd); /* 연보라 */
}
.slide-bg-pink {
  background: linear-gradient(-135deg, #ffe4e6, #f9a8d4); /* 연핑크 */
}



.slide-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.05)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.05)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
  opacity: 0.1;
}

.slide-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  position: relative;
  z-index: 1;
}

.content-wrapper {
  flex: 1;
  max-width: 500px;
  animation: slideInLeft 1s ease-out;
}

.slide-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: white;
  margin: 0 0 0.8rem 0;
  line-height: 1.2;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  animation: fadeInUp 1s ease-out 0.2s both;
}
.slide-title,
.slide-description {
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3); /* 기존보다 강하게 */
}

.slide-description {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 1.5rem 0;
  line-height: 1.6;
  animation: fadeInUp 1s ease-out 0.4s both;
}

.cta-button {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  color: #10b981;
  border: none;
  padding: 1rem 2rem;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  animation: fadeInUp 1s ease-out 0.6s both;
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
}

.button-arrow {
  transition: transform 0.3s ease;
}

.cta-button:hover .button-arrow {
  transform: translateX(4px);
}

.slide-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  animation: slideInRight 1s ease-out;
}

.slide-image img {
  max-width: 300px;
  max-height: 300px;
  object-fit: contain;
  filter: drop-shadow(0 20px 40px rgba(0, 0, 0, 0.1));
  animation: float 6s ease-in-out infinite;
}

.image-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.2) 0%, transparent 70%);
  border-radius: 50%;
  animation: glow 4s ease-in-out infinite alternate;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

@keyframes glow {
  0% { opacity: 0.3; transform: translate(-50%, -50%) scale(1); }
  100% { opacity: 0.6; transform: translate(-50%, -50%) scale(1.1); }
}

@keyframes slideInLeft {
  from { opacity: 0; transform: translateX(-50px); }
  to { opacity: 1; transform: translateX(0); }
}

@keyframes slideInRight {
  from { opacity: 0; transform: translateX(50px); }
  to { opacity: 1; transform: translateX(0); }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 캐러셀 컨트롤 */
.carousel-controls {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 2rem;
}

.carousel-dots {
  display: flex;
  gap: 0.5rem;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.dot.active {
  background: white;
  transform: scale(1.2);
}

.carousel-nav {
  display: flex;
  gap: 0.5rem;
}

.nav-btn {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

/* 메인 콘텐츠 */
.main-content {
  position: relative;
  z-index: 2;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* 소개 섹션 */
.intro-section {
  padding: 3rem 0;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-title {
  font-size: 2.2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #1e40af 0%, #10b981 50%, #059669 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0 0 0.8rem 0;
  animation: fadeInUp 0.8s ease-out;
}

.section-subtitle {
  font-size: 1rem;
  color: #6b7280;
  margin: 0;
  animation: fadeInUp 0.8s ease-out 0.2s both;
}

.intro-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.intro-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  padding: 2rem;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  animation: fadeInUp 0.8s ease-out both;
}

.intro-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.12);
}

.card-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  font-size: 1.5rem;
  color: white;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
}

.card-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 0.8rem 0;
}

.card-description {
  font-size: 0.95rem;
  color: #6b7280;
  line-height: 1.6;
  margin: 0;
}

/* 캐릭터 섹션 */
.character-section {
  padding: 4rem 0;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  position: relative;
  overflow: hidden;
}

.character-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="rgba(16,185,129,0.05)"/><circle cx="80" cy="80" r="2" fill="rgba(16,185,129,0.05)"/></svg>');
  opacity: 0.5;
}

.character-content {
  display: flex;
  align-items: center;
  gap: 4rem;
  position: relative;
  z-index: 1;
}

.character-info {
  flex: 1;
}

.character-description {
  font-size: 1.2rem;
  color: #374151;
  line-height: 1.8;
  margin: 0 0 2rem 0;
}

.character-features {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 1.1rem;
  color: #374151;
  font-weight: 500;
}

.feature-icon {
  font-size: 1.5rem;
  width: 40px;
  text-align: center;
}

.character-visual {
  flex: 1;
  display: flex;
  justify-content: center;
}

.character-circle {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 20px 60px rgba(16, 185, 129, 0.2);
  border: 4px solid rgba(16, 185, 129, 0.1);
  animation: characterFloat 8s ease-in-out infinite;
}

@keyframes characterFloat {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  25% { transform: translateY(-10px) rotate(1deg); }
  50% { transform: translateY(0) rotate(0deg); }
  75% { transform: translateY(-5px) rotate(-1deg); }
}

.character-image {
  max-width: 200px;
  max-height: 200px;
  object-fit: contain;
}

/* 서비스 섹션 */
.services-section {
  padding: 4rem 0;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.service-card {
  position: relative;
  border-radius: 24px;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  min-height: 300px;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  overflow: hidden;
}

.service-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.12);
}

.card-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  transition: all 0.3s ease;
  border-radius: 24px;
}

/* 각 카드별 배경 그라디언트 */
.service-card.community .card-background {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  opacity: 0.1;
}

.service-card.finance .card-background {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  opacity: 0.1;
}

.service-card.bank .card-background {
  background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
  opacity: 0.1;
}

.service-card:hover .card-background {
  opacity: 0.15;
}

/* 배경 패턴 */
.bg-pattern {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 60"><defs><pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="1.5" fill="rgba(59,130,246,0.1)"/></pattern></defs><rect width="60" height="60" fill="url(%23dots)"/></svg>');
  opacity: 0.3;
}

/* 떠다니는 도형들 */
.floating-shapes {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

.shape {
  position: absolute;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 50%;
  animation: gentleFloat 12s ease-in-out infinite;
}

.shape-1 {
  width: 40px;
  height: 40px;
  top: 15%;
  right: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 25px;
  height: 25px;
  top: 70%;
  right: 25%;
  animation-delay: 4s;
}

.shape-3 {
  width: 15px;
  height: 15px;
  top: 40%;
  right: 70%;
  animation-delay: 8s;
}

@keyframes gentleFloat {
  0%, 100% {
    transform: translateY(0);
    opacity: 0.3;
  }
  50% {
    transform: translateY(-8px);
    opacity: 0.5;
  }
}

.card-content {
  position: relative;
  z-index: 2;
  padding: 2rem;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.service-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  color: white;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
  transition: all 0.3s ease;
}

.service-card.community .service-icon {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
}

.service-card.finance .service-icon {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
}

.service-card.bank .service-icon {
  background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
  box-shadow: 0 4px 16px rgba(245, 158, 11, 0.3);
}

.service-card:hover .service-icon {
  transform: scale(1.1);
}

.service-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 0.8rem 0;
  letter-spacing: -0.025em;
}

.service-description {
  font-size: 1rem;
  color: #6b7280;
  margin: 0 0 1rem 0;
  line-height: 1.6;
  flex-grow: 1;
}

.service-stats,
.service-location,
.service-badge {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.badge {
  padding: 0.25rem 0.6rem;
  border-radius: 8px;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.badge.new {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  color: white;
}

.badge.hot {
  background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
  color: white;
}

.service-arrow {
  position: absolute;
  bottom: 1rem;
  right: 1.5rem;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: #6b7280;
  transition: all 0.3s ease;
  opacity: 0;
  transform: scale(0.9);
}

.service-card:hover .service-arrow {
  opacity: 1;
  transform: scale(1);
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
}

/* 하단 정보 섹션 */
.bottom-info-section {
  padding: 4rem 0;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
}

.info-panel {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.info-panel:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.12);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid rgba(59, 130, 246, 0.1);
}

.panel-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.panel-title i {
  color: #3b82f6;
}

.view-more-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.view-more-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.notice-list, .popular-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.notice-item, .popular-item {
  padding: 1rem 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  cursor: pointer;
  transition: all 0.2s ease;
}

.notice-item:hover, .popular-item:hover {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  margin: 0 -1rem;
  padding: 1rem;
  border-radius: 8px;
  border-bottom: 1px solid transparent;
}

.notice-item:last-child, .popular-item:last-child {
  border-bottom: none;
}

.notice-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notice-title {
  font-weight: 500;
  color: #374151;
  flex: 1;
}

.notice-date {
  font-size: 0.85rem;
  color: #9ca3af;
  margin-left: 1rem;
}

.post-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.post-title {
  font-weight: 500;
  color: #374151;
  line-height: 1.4;
}

.post-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
}

.post-likes, .post-comments {
  color: #9ca3af;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

/* 푸터 */
.main-footer {
  background: linear-gradient(135deg, rgb(255, 255, 255) 0%, white 100%);
  color: white;
  padding: 3rem 0;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-logo {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.logo-text {
  font-size: 2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.logo-subtitle {
  font-size: 0.9rem;
  color: #9ca3af;
}

.footer-copy {
  color: #9ca3af;
  font-size: 0.9rem;
}

/* 반응형 디자인 */
@media (max-width: 1024px) {
  .slide-content {
    flex-direction: column;
    text-align: center;
    gap: 1.5rem;
  }
  
  .content-wrapper {
    max-width: none;
  }
  
  .slide-title {
    font-size: 2rem;
  }
  
  .character-content {
    flex-direction: column;
    gap: 2rem;
    text-align: center;
  }
  
  .intro-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.2rem;
  }
  
  .services-grid {
    grid-template-columns: 1fr;
    gap: 1.2rem;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }
  
  .hero-section {
    height: 40vh;
    min-height: 350px;
  }
  
  .slide-title {
    font-size: 1.8rem;
  }
  
  .slide-description {
    font-size: 1rem;
  }
  
  .section-title {
    font-size: 1.8rem;
  }
  
  .intro-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .intro-card {
    padding: 1.5rem;
  }
  
  .character-circle {
    width: 200px;
    height: 200px;
  }
  
  .character-image {
    max-width: 120px;
    max-height: 120px;
  }
  
  .service-card {
    min-height: 240px;
  }
  
  .card-content {
    padding: 1.5rem;
  }
  
  .service-title {
    font-size: 1.2rem;
  }
  
  .info-panel {
    padding: 1.5rem;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .slide-title {
    font-size: 1.6rem;
  }
  
  .carousel-controls {
    bottom: 0.8rem;
  }
  
  .character-features {
    gap: 0.6rem;
  }
  
  .feature-item {
    font-size: 0.9rem;
  }
  
  .notice-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.4rem;
  }
  
  .notice-date {
    margin-left: 0;
  }
  
  .intro-section, .character-section, .services-section, .bottom-info-section {
    padding: 2rem 0;
  }
}
</style>