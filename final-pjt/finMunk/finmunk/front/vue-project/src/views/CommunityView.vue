<template>
  <div class="community-container">
    <!-- 배경 장식 -->
    <div class="bg-decorations">
      <span class="floating-item" v-for="n in 6" :key="n">{{ n % 2 === 0 ? '🌰' : '🍃' }}</span>
    </div>

    <!-- 헤더 섹션 -->
    <header class="community-header">
      <div class="header-content">
        <h1 class="page-title">
          <span class="title-icon wiggle">💬</span>
          다람쥐들의 수다방
          <span class="squirrel-badge bounce">🐿️</span>
        </h1>
        <p class="page-subtitle">함께 나누는 금융 이야기</p>
      </div>

      <!-- 카테고리 & 액션 바 -->
      <div class="action-bar">
        <div class="category-wrapper">
          <span class="category-icon">📂</span>
          <select v-model="selectedCategory" @change="loadByCategory" class="category-select">
            <option value="">🌈 전체 보기</option>
            <option value="notice">📢 공지사항</option>
            <option value="event">🎉 이벤트</option>
            <option value="tip">💡 자유게시판</option>
          </select>
        </div>

        <RouterLink v-if="userStore.user" :to="{ name: 'CommunityWrite' }" class="write-btn">
          <span class="btn-icon bounce">✍️</span>
          글쓰기
        </RouterLink>
      </div>
    </header>

    <!-- 게시글 목록 -->
    <main class="articles-section">
      <TransitionGroup name="list-fade" tag="div" class="articles-grid">
        <article
          v-for="article in communityStore.articles"
          :key="article.id"
          class="article-preview"
        >
          <Articleitem :article="article" />
        </article>
      </TransitionGroup>

      <!-- 게시글이 없을 때 -->
      <div v-if="!communityStore.articles?.length" class="empty-state">
        <span class="empty-icon">🐿️</span>
        <h3>아직 게시글이 없어요!</h3>
        <p>첫 번째 게시글을 작성해보세요 🌰</p>
      </div>
    </main>

    <!-- 플로팅 메뉴 -->
    <div class="floating-menu">
      <button class="scroll-top-btn" @click="scrollToTop">
        <span>🔝</span>
        <span class="tooltip">맨 위로</span>
      </button>
    </div>

    <!-- 챗봇 -->
    <Chatbot />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useCommunityStore } from '@/stores/community'
import Articleitem from '@/components/community/Articleitem.vue'
import Chatbot from '@/components/chatbot/Chatbot.vue'

const userStore = useUserStore()
const communityStore = useCommunityStore()

const selectedCategory = ref('')

// 카테고리별 게시글 불러오기
const loadByCategory = () => {
  communityStore.loadArticles(selectedCategory.value)
}

// 맨 위로 스크롤
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  loadByCategory()
})
</script>

<style scoped>
/* 기본 컨테이너 */
.community-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  position: relative;
}

/* 배경 장식 */
.bg-decorations {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: -1;
  overflow: hidden;
}

.floating-item {
  position: absolute;
  font-size: 2.5rem;
  opacity: 0.1;
  animation: gentleFloat 20s infinite ease-in-out;
}

.floating-item:nth-child(1) { top: 10%; left: 10%; animation-delay: 0s; }
.floating-item:nth-child(2) { top: 20%; left: 80%; animation-delay: 3s; }
.floating-item:nth-child(3) { top: 50%; left: 20%; animation-delay: 6s; }
.floating-item:nth-child(4) { top: 70%; left: 70%; animation-delay: 9s; }
.floating-item:nth-child(5) { top: 30%; left: 50%; animation-delay: 12s; }
.floating-item:nth-child(6) { top: 80%; left: 90%; animation-delay: 15s; }

@keyframes gentleFloat {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  25% {
    transform: translateY(-30px) rotate(90deg);
  }
  50% {
    transform: translateY(0) rotate(180deg);
  }
  75% {
    transform: translateY(30px) rotate(270deg);
  }
}

/* 헤더 섹션 */
.community-header {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  border-radius: 30px;
  padding: 40px;
  margin-bottom: 40px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  animation: slideDown 0.6s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.header-content {
  text-align: center;
  margin-bottom: 30px;
}

.page-title {
  font-size: 2.5rem;
  color: #2c3e50;
  margin: 0 0 10px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.title-icon {
  display: inline-block;
  font-size: 2.5rem;
}

.squirrel-badge {
  display: inline-block;
  background: white;
  border-radius: 50%;
  padding: 5px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
}

.page-subtitle {
  font-size: 1.2rem;
  color: #555;
  margin: 0;
}

/* 액션 바 */
.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(10px);
  padding: 15px 25px;
  border-radius: 20px;
}

.category-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  background: white;
  padding: 8px 15px;
  border-radius: 15px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
}

.category-icon {
  font-size: 1.3rem;
}

.category-select {
  border: none;
  background: none;
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  cursor: pointer;
  padding: 5px 10px;
  outline: none;
}

.category-select option {
  background: white;
  color: #333;
  padding: 10px;
}

.write-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #4CAF50;
  color: white;
  padding: 12px 24px;
  border-radius: 25px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s;
  box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
}

.write-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(76, 175, 80, 0.4);
  background: #45a049;
}

.btn-icon {
  display: inline-block;
  font-size: 1.2rem;
}

/* 게시글 목록 */
.articles-section {
  min-height: 400px;
}

.articles-grid {
  display: grid;
  gap: 20px;
}

.article-preview {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
  animation: fadeInUp 0.6s ease-out backwards;
  position: relative;
}

.article-preview::before {
  content: '🌰';
  position: absolute;
  top: -10px;
  right: 20px;
  font-size: 2rem;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s;
}

.article-preview:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.article-preview:hover::before {
  opacity: 0.8;
  transform: translateY(0);
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

.article-preview:nth-child(1) { animation-delay: 0.1s; }
.article-preview:nth-child(2) { animation-delay: 0.2s; }
.article-preview:nth-child(3) { animation-delay: 0.3s; }
.article-preview:nth-child(4) { animation-delay: 0.4s; }
.article-preview:nth-child(5) { animation-delay: 0.5s; }

/* 빈 상태 */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  animation: fadeIn 0.6s ease-out;
}

.empty-icon {
  font-size: 5rem;
  display: block;
  margin-bottom: 20px;
  animation: bounce 2s infinite;
}

.empty-state h3 {
  font-size: 1.5rem;
  color: #333;
  margin: 0 0 10px 0;
}

.empty-state p {
  color: #666;
  font-size: 1.1rem;
}

/* 플로팅 메뉴 */
.floating-menu {
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: 100;
}

.scroll-top-btn {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
  transition: all 0.3s;
  position: relative;
}

.scroll-top-btn:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5);
}

.tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: #333;
  color: white;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 0.9rem;
  white-space: nowrap;
  margin-bottom: 10px;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s;
}

.scroll-top-btn:hover .tooltip {
  opacity: 1;
}

/* 트랜지션 */
.list-fade-enter-active,
.list-fade-leave-active {
  transition: all 0.5s ease;
}

.list-fade-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.list-fade-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

/* 애니메이션 클래스 */
.bounce {
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.wiggle {
  animation: wiggle 2s infinite;
}

@keyframes wiggle {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-10deg); }
  75% { transform: rotate(10deg); }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .community-container {
    padding: 10px;
  }

  .community-header {
    padding: 25px 20px;
    border-radius: 20px;
  }

  .page-title {
    font-size: 1.8rem;
    flex-wrap: wrap;
  }

  .page-subtitle {
    font-size: 1rem;
  }

  .action-bar {
    flex-direction: column;
    gap: 15px;
    padding: 15px;
  }

  .category-wrapper {
    width: 100%;
    justify-content: center;
  }

  .write-btn {
    width: 100%;
    justify-content: center;
  }

  .floating-menu {
    bottom: 20px;
    right: 20px;
  }

  .scroll-top-btn {
    width: 50px;
    height: 50px;
    font-size: 1.3rem;
  }
}

/* 다크 모드 지원 */
@media (prefers-color-scheme: dark) {
  .community-container {
    background: #1a1a1a;
  }

  .article-preview {
    background: #2a2a2a;
  }

  .empty-state h3 {
    color: #f0f0f0;
  }

  .empty-state p {
    color: #b0b0b0;
  }

  .category-select {
    background: #333;
    color: #f0f0f0;
  }

  .category-wrapper {
    background: #333;
  }
}

/* 로딩 애니메이션 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>