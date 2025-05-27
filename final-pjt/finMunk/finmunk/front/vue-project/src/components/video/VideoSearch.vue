<template>
  <div class="search-page">
    <!-- 검색 헤더 -->
    <div class="search-header">
      <div class="header-icon">
        <i class="fas fa-video"></i>
      </div>
      <div class="header-content">
        <h1 class="page-title">🎬 관심 종목 비디오 검색</h1>
        <p class="page-subtitle">원하는 영상을 찾아보세요</p>
      </div>
    </div>

    <!-- 검색 입력 영역 -->
    <div class="search-container">
      <div class="search-box">
        <div class="search-icon">
          <i class="fas fa-search"></i>
        </div>
        <input 
          v-model="query" 
          @keyup.enter="searchVideos"
          @input="onInputChange"
          placeholder="검색어를 입력하세요..."
          class="search-input"
        />
        <button 
          v-if="query"
          @click="clearSearch"
          class="clear-btn"
        >
          <i class="fas fa-times"></i>
        </button>
      </div>
      <button 
        @click="searchVideos" 
        :disabled="!query.trim()"
        class="search-btn"
      >
        <i class="fas fa-search"></i>
        검색
      </button>
    </div>

    <!-- 검색 결과 상태 -->
    <div v-if="isLoading" class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">영상을 검색하고 있습니다...</p>
    </div>

    <!-- 검색 결과 없음 -->
    <div v-else-if="hasSearched && videos.length === 0" class="no-results">
      <div class="no-results-icon">🔍</div>
      <h3 class="no-results-title">검색 결과가 없습니다</h3>
      <p class="no-results-description">다른 키워드로 다시 검색해보세요</p>
    </div>

    <!-- 검색 결과 -->
    <div v-else-if="videos.length > 0" class="results-section">
      <div class="results-header">
        <h2 class="results-title">검색 결과</h2>
        <span class="results-count">{{ videos.length }}개의 영상</span>
      </div>

      <div class="video-grid">
        <div 
          v-for="(video, index) in paginatedVideos" 
          :key="video.id.videoId"
          class="video-item"
        >
          <!-- 비디오 카드 -->
          <router-link 
            :to="`/videos/detail/${video.id.videoId}`" 
            class="video-link"
          >
            <div class="video-card">
              <!-- 썸네일 -->
              <div class="video-thumbnail">
                <img 
                  :src="video.snippet.thumbnails.medium.url" 
                  :alt="video.snippet.title"
                  class="thumbnail-img"
                />
                <div class="video-overlay">
                  <div class="play-icon">
                    <i class="fas fa-play"></i>
                  </div>
                </div>
                <div class="video-duration">
                  {{ formatDuration(video.contentDetails?.duration) }}
                </div>
              </div>

              <!-- 비디오 정보 -->
              <div class="video-info">
                <h3 class="video-title">{{ video.snippet.title }}</h3>
                <div class="video-meta">
                  <span class="channel-name">{{ video.snippet.channelTitle }}</span>
                  <span class="publish-date">{{ formatDate(video.snippet.publishedAt) }}</span>
                </div>
                <p class="video-description">{{ truncateDescription(video.snippet.description) }}</p>
              </div>
            </div>
          </router-link>

          <!-- 액션 버튼 -->
          <div class="video-actions">
            <button 
              @click="saveToWatchLater(video)"
              :disabled="isAlreadySaved(video.id.videoId)"
              class="save-btn"
              :class="{ 'saved': isAlreadySaved(video.id.videoId) }"
            >
              <i class="fas" :class="isAlreadySaved(video.id.videoId) ? 'fa-bookmark' : 'fa-bookmark-o'"></i>
              {{ isAlreadySaved(video.id.videoId) ? '저장됨' : '나중에 보기' }}
            </button>
          </div>
        </div>
      </div>
    </div>

  <div class="pagination" v-if="totalPages > 1">
    <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">이전</button>

    <button 
      v-for="page in totalPages" 
      :key="page" 
      @click="goToPage(page)" 
      :class="{ active: currentPage === page }"
    >
      {{ page }}
    </button>

    <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages">다음</button>
  </div>


    <!-- 초기 상태 (검색 전) -->
    <div v-else class="initial-state">
      <div class="initial-icon">🎯</div>
      <h3 class="initial-title">관심 종목 관련 영상을 검색해보세요</h3>
      <p class="initial-description">관심 있는 종목을 입력하여 관련 영상을 찾아보세요</p>
      <div class="popular-searches">
        <h4>인기 검색어</h4>
        <div class="search-tags">
          <button 
            v-for="tag in popularTags" 
            :key="tag"
            @click="searchWithTag(tag)"
            class="search-tag"
          >
            {{ tag }}
          </button>
        </div>
      </div>
    </div>

    <!-- 성공 토스트 -->
    <div v-if="showToast" class="toast" :class="toastType">
      <i class="fas" :class="toastType === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'"></i>
      {{ toastMessage }}
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, computed } from 'vue'

const query = ref('')
const videos = ref([])
const isLoading = ref(false)
const hasSearched = ref(false)
const showToast = ref(false)
const toastMessage = ref('')
const toastType = ref('success')
const savedVideos = ref([])
const API_URL = import.meta.env.VITE_API_URL

const popularTags = ['삼성전자', 'SK하이닉스', '현대차', 'KB금융', '한화에어로스페이스', '기아']

const searchVideos = async () => {
  if (!query.value.trim()) return
  
  isLoading.value = true
  hasSearched.value = true
  
  try {
    const res = await axios.get(`${API_URL}/videos/`, { params: { q: query.value } })
    videos.value = res.data.items
  } catch (err) {
    console.error('서버 API 에러:', err)
    showToastMessage('검색 중 오류가 발생했습니다', 'error')
  } finally {
    isLoading.value = false
  }
}

const currentPage = ref(1)
const itemsPerPage = 6

const paginatedVideos = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return videos.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(videos.value.length / itemsPerPage)
})

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}


const searchWithTag = (tag) => {
  query.value = tag
  searchVideos()
}

const clearSearch = () => {
  query.value = ''
  videos.value = []
  hasSearched.value = false
}

const onInputChange = () => {
  if (!query.value.trim()) {
    videos.value = []
    hasSearched.value = false
  }
}

const saveToWatchLater = (video) => {
  const saved = JSON.parse(localStorage.getItem('watchLater') || '[]')
  const exists = saved.find(v => v.id.videoId === video.id.videoId)
  
  if (!exists) {
    const videoWithDate = { ...video, savedAt: new Date().toISOString() }
    saved.push(videoWithDate)
    localStorage.setItem('watchLater', JSON.stringify(saved))
    savedVideos.value = saved
    showToastMessage('영상이 저장되었습니다!', 'success')
  } else {
    showToastMessage('이미 저장된 영상입니다', 'warning')
  }
}

const isAlreadySaved = (videoId) => {
  const saved = JSON.parse(localStorage.getItem('watchLater') || '[]')
  return saved.some(v => v.id.videoId === videoId)
}

const showToastMessage = (message, type = 'success') => {
  toastMessage.value = message
  toastType.value = type
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const formatDuration = (duration) => {
  if (!duration) return ''
  // ISO 8601 duration을 분:초 형태로 변환
  const match = duration.match(/PT(\d+H)?(\d+M)?(\d+S)?/)
  if (!match) return ''
  
  const hours = parseInt(match[1]) || 0
  const minutes = parseInt(match[2]) || 0
  const seconds = parseInt(match[3]) || 0
  
  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
  }
  return `${minutes}:${seconds.toString().padStart(2, '0')}`
}

const truncateDescription = (description) => {
  if (!description) return ''
  return description.length > 120 ? description.substring(0, 120) + '...' : description
}
</script>

<style scoped>
.search-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

/* 검색 헤더 */
.search-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 40px;
  padding: 24px;
  background: linear-gradient(135deg, #4DD0B1 0%, #3CBFA0 100%);
  border-radius: 20px;
  color: white;
  box-shadow: 0 8px 32px rgba(77, 208, 177, 0.3);
}

.header-icon {
  width: 64px;
  height: 64px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  backdrop-filter: blur(10px);
}

.header-content {
  flex: 1;
}

.page-title {
  font-size: 28px;
  font-weight: 800;
  margin: 0 0 8px 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.page-subtitle {
  font-size: 16px;
  margin: 0;
  opacity: 0.9;
  font-weight: 500;
}

/* 검색 입력 영역 */
.search-container {
  display: flex;
  gap: 16px;
  margin-bottom: 40px;
  animation: fadeInUp 0.6s ease-out;
}

.search-box {
  flex: 1;
  position: relative;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.search-box:focus-within {
  border-color: #4DD0B1;
  box-shadow: 0 8px 32px rgba(77, 208, 177, 0.2);
}

.search-icon {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
  font-size: 18px;
}

.search-input {
  width: 100%;
  padding: 18px 20px 18px 56px;
  border: none;
  outline: none;
  font-size: 16px;
  background: transparent;
  border-radius: 16px;
}

.search-input::placeholder {
  color: #9ca3af;
}

.clear-btn {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 32px;
  height: 32px;
  border: none;
  background: #f3f4f6;
  border-radius: 50%;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-btn:hover {
  background: #e5e7eb;
  color: #374151;
}

.search-btn {
  background: linear-gradient(135deg, #4DD0B1 0%, #3CBFA0 100%);
  color: white;
  border: none;
  padding: 18px 32px;
  border-radius: 16px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 16px rgba(77, 208, 177, 0.3);
  white-space: nowrap;
}

.search-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(77, 208, 177, 0.4);
}

.search-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top: 4px solid #4DD0B1;
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

/* 검색 결과 없음 */
.no-results {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.no-results-icon {
  font-size: 80px;
  margin-bottom: 24px;
}

.no-results-title {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 12px 0;
}

.no-results-description {
  font-size: 16px;
  color: #6b7280;
  margin: 0;
}

/* 검색 결과 섹션 */
.results-section {
  animation: fadeInUp 0.6s ease-out;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 0 4px;
}

.results-title {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.results-count {
  font-size: 14px;
  color: #6b7280;
  background: white;
  padding: 8px 16px;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 비디오 그리드 */
.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.video-item {
  animation: fadeInUp 0.6s ease-out both;
}

.video-link {
  text-decoration: none;
  color: inherit;
}

.video-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

.video-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
}

/* 썸네일 */
.video-thumbnail {
  position: relative;
  width: 100%;
  height: 180px;
  overflow: hidden;
}

.thumbnail-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.video-card:hover .thumbnail-img {
  transform: scale(1.05);
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.4) 0%, rgba(0, 0, 0, 0.2) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.video-card:hover .video-overlay {
  opacity: 1;
}

.play-icon {
  width: 56px;
  height: 56px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: #4DD0B1;
  transform: scale(0.8);
  transition: transform 0.3s ease;
}

.video-card:hover .play-icon {
  transform: scale(1);
}

.video-duration {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

/* 비디오 정보 */
.video-info {
  padding: 20px;
}

.video-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 12px 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.video-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  font-size: 12px;
  color: #6b7280;
}

.channel-name {
  font-weight: 500;
  color: #4DD0B1;
}

.video-description {
  font-size: 13px;
  color: #6b7280;
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 액션 버튼 */
.video-actions {
  padding: 0 20px 20px;
}

.save-btn {
  width: 100%;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: linear-gradient(135deg, #4DD0B1 0%, #3CBFA0 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(77, 208, 177, 0.3);
}

.save-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(77, 208, 177, 0.4);
}

.save-btn.saved {
  background: #f3f4f6;
  color: #6b7280;
  box-shadow: none;
}

.save-btn:disabled {
  cursor: not-allowed;
}

/* 초기 상태 */
.initial-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  animation: fadeInUp 0.6s ease-out;
}

.initial-icon {
  font-size: 80px;
  margin-bottom: 24px;
}

.initial-title {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 12px 0;
}

.initial-description {
  font-size: 16px;
  color: #6b7280;
  margin: 0 0 32px 0;
  line-height: 1.6;
}

.popular-searches h4 {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 16px 0;
}

.search-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.search-tag {
  background: #f8fafc;
  color: #4DD0B1;
  border: 1px solid #e2e8f0;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.search-tag:hover {
  background: #4DD0B1;
  color: white;
  border-color: #4DD0B1;
}

/* 토스트 메시지 */
.toast {
  position: fixed;
  top: 100px;
  right: 20px;
  padding: 16px 24px;
  border-radius: 12px;
  color: white;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  z-index: 1000;
  animation: slideInRight 0.3s ease-out;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.toast.success {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.toast.warning {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.toast.error {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.pagination {
  display: flex;
  gap: 8px;
  justify-content: center;
  margin-top: 24px;
}

.pagination button {
  padding: 8px 14px;
  border-radius: 8px;
  border: none;
  background-color: #f3f4f6;
  cursor: pointer;
  font-weight: 600;
}

.pagination button.active {
  background-color: #4DD0B1;
  color: white;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}


@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
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
@media (max-width: 768px) {
  .search-page {
    padding: 20px 16px;
  }
  
  .search-header {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
  
  .search-container {
    flex-direction: column;
  }
  
  .video-grid {
    grid-template-columns: 1fr;
  }
  
  .results-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .search-tags {
    gap: 6px;
  }
  
  .search-tag {
    font-size: 12px;
    padding: 6px 12px;
  }
}
</style>