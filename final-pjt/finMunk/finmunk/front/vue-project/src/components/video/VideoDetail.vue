<template>
  <div class="video-detail-page">
    <!-- 네비게이션 헤더 -->
    <div class="nav-header">
      <button @click="$router.push('/videos')" class="back-btn">
        <i class="fas fa-arrow-left"></i>
        뒤로가기
      </button>
      <div class="breadcrumb">
        <span class="breadcrumb-item">비디오</span>
        <i class="fas fa-chevron-right"></i>
        <span class="breadcrumb-current">상세보기</span>
      </div>
    </div>

    <!-- 로딩 상태 -->
    <div v-if="isLoading" class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">영상 정보를 불러오고 있습니다...</p>
    </div>

    <!-- 메인 콘텐츠 -->
    <div v-else class="video-content">
      <!-- 비디오 플레이어 섹션 -->
      <div class="video-player-section">
        <div class="video-container">
          <iframe
            :src="`https://www.youtube.com/embed/${videoId}`"
            frameborder="0"
            allowfullscreen
            class="video-iframe"
          ></iframe>
        </div>
        
        <!-- 비디오 정보 -->
        <div class="video-info-section">
          <div class="video-header">
            <h1 class="video-title">{{ video.snippet?.title }}</h1>
            <div class="video-actions">
              <button 
                @click="toggleSave" 
                class="action-btn save-btn"
                :class="{ 'saved': isSaved }"
              >
                <i class="fas" :class="isSaved ? 'fa-bookmark' : 'fa-bookmark-o'"></i>
                {{ isSaved ? '저장됨' : '저장하기' }}
              </button>
              <button @click="shareVideo" class="action-btn share-btn">
                <i class="fas fa-share"></i>
                공유하기
              </button>
            </div>
          </div>

          <div class="video-meta">
            <div class="meta-item">
              <i class="fas fa-user"></i>
              <span class="channel-name">{{ video.snippet?.channelTitle }}</span>
            </div>
            <div class="meta-item">
              <i class="fas fa-calendar"></i>
              <span class="publish-date">{{ formatDate(video.snippet?.publishedAt) }}</span>
            </div>
            <div class="meta-item" v-if="video.statistics">
              <i class="fas fa-eye"></i>
              <span class="view-count">{{ formatViewCount(video.statistics.viewCount) }}</span>
            </div>
          </div>

          <!-- 영상 설명 -->
          <div class="video-description" v-if="video.snippet?.description">
            <h3 class="description-title">영상 설명</h3>
            <div class="description-content" :class="{ 'expanded': showFullDescription }">
              <p>{{ video.snippet.description }}</p>
            </div>
            <button 
              v-if="video.snippet.description.length > 200"
              @click="showFullDescription = !showFullDescription"
              class="toggle-description-btn"
            >
              {{ showFullDescription ? '접기' : '더보기' }}
            </button>
          </div>
        </div>
      </div>

      <!-- AI 요약 섹션 -->
      <div class="ai-summary-section">
        <div class="summary-header">
          <div class="ai-icon">
            <i class="fas fa-brain"></i>
          </div>
          <div class="summary-title">
            <h3>🧠 ChatGPT 영상 요약</h3>
            <span class="ai-badge">AI 분석</span>
          </div>
          <button 
            v-if="!summary && !summaryLoading"
            @click="fetchSummary"
            class="retry-btn"
          >
            <i class="fas fa-redo"></i>
            다시 시도
          </button>
        </div>

        <div class="summary-content">
          <!-- 로딩 상태 -->
          <div v-if="summaryLoading" class="summary-loading">
            <div class="summary-spinner"></div>
            <p>AI가 영상을 분석하고 있습니다...</p>
          </div>

          <!-- 요약 결과 -->
          <div v-else-if="summary" class="summary-result">
            <p>{{ summary }}</p>
            <div class="summary-footer">
              <span class="summary-note">
                <i class="fas fa-info-circle"></i>
                AI가 생성한 요약으로 실제 내용과 다를 수 있습니다
              </span>
            </div>
          </div>

          <!-- 요약 실패 -->
          <div v-else class="summary-error">
            <div class="error-icon">🤖</div>
            <h4>요약을 생성할 수 없습니다</h4>
            <p>자막이 없거나 처리할 수 없는 영상입니다</p>
          </div>
        </div>
      </div>

      <!-- 관련 영상 섹션 (옵션) -->
      <div class="related-videos-section" v-if="relatedVideos.length > 0">
        <h3 class="section-title">관련 영상</h3>
        <div class="related-videos-grid">
          <div 
            v-for="relatedVideo in relatedVideos" 
            :key="relatedVideo.id.videoId"
            class="related-video-card"
            @click="navigateToVideo(relatedVideo.id.videoId)"
          >
            <img 
              :src="relatedVideo.snippet.thumbnails.medium.url" 
              :alt="relatedVideo.snippet.title"
              class="related-thumbnail"
            />
            <div class="related-info">
              <h4 class="related-title">{{ relatedVideo.snippet.title }}</h4>
              <p class="related-channel">{{ relatedVideo.snippet.channelTitle }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 성공 토스트 -->
    <div v-if="showToast" class="toast" :class="toastType">
      <i class="fas" :class="getToastIcon()"></i>
      {{ toastMessage }}
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const videoId = route.params.videoId

const video = ref({})
const isSaved = ref(false)
const summary = ref('')
const isLoading = ref(true)
const summaryLoading = ref(false)
const showFullDescription = ref(false)
const relatedVideos = ref([])
const showToast = ref(false)
const toastMessage = ref('')
const toastType = ref('success')

const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY

const fetchVideoDetail = async () => {
  try {
    const res = await fetch(`https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id=${videoId}&key=${API_KEY}`)
    const data = await res.json()
    if (data.items && data.items.length > 0) {
      video.value = data.items[0]
    }
  } catch (error) {
    console.error('영상 정보 로드 실패:', error)
    showToastMessage('영상 정보를 불러올 수 없습니다', 'error')
  }
}

const fetchSummary = async () => {
  summaryLoading.value = true
  try {
    const res = await axios.get(`${import.meta.env.VITE_API_URL}/videos/summarize-video/`, {
      params: {
        video_id: videoId,
        title: video.value.snippet?.title || '',
        description: video.value.snippet?.description || ''
      }
    })
    summary.value = res.data.summary
  } catch (err) {
    console.error('🔥 요약 실패:', err)
    summary.value = ''
  } finally {
    summaryLoading.value = false
  }
}

const toggleSave = async () => {
  try {
    if (isSaved.value) {
      await axios.delete(`${import.meta.env.VITE_API_URL}/videos/save/`, {
        data: { videoId }
      })
      // 로컬스토리지에서도 제거
      const saved = JSON.parse(localStorage.getItem('savedVideos') || '[]')
      const filtered = saved.filter(id => id !== videoId)
      localStorage.setItem('savedVideos', JSON.stringify(filtered))
      
      showToastMessage('저장이 취소되었습니다', 'info')
    } else {
      await axios.post(`${import.meta.env.VITE_API_URL}/videos/save/`, {
        videoId,
        snippet: video.value.snippet
      })
      // 로컬스토리지에도 추가
      const saved = JSON.parse(localStorage.getItem('savedVideos') || '[]')
      if (!saved.includes(videoId)) {
        saved.push(videoId)
        localStorage.setItem('savedVideos', JSON.stringify(saved))
      }
      
      showToastMessage('영상이 저장되었습니다!', 'success')
    }
    isSaved.value = !isSaved.value
  } catch (err) {
    console.error('저장 처리 실패:', err)
    showToastMessage('저장 처리 중 오류가 발생했습니다', 'error')
  }
}

const shareVideo = async () => {
  const shareData = {
    title: video.value.snippet?.title,
    text: `${video.value.snippet?.title} - YouTube`,
    url: `https://www.youtube.com/watch?v=${videoId}`
  }

  if (navigator.share) {
    try {
      await navigator.share(shareData)
    } catch (err) {
      copyToClipboard(shareData.url)
    }
  } else {
    copyToClipboard(shareData.url)
  }
}

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    showToastMessage('링크가 복사되었습니다!', 'success')
  } catch (err) {
    showToastMessage('링크 복사에 실패했습니다', 'error')
  }
}

const navigateToVideo = (newVideoId) => {
  router.push(`/videos/detail/${newVideoId}`)
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatViewCount = (count) => {
  if (!count) return ''
  const num = parseInt(count)
  if (num >= 1000000) {
    return `${(num / 1000000).toFixed(1)}M회`
  } else if (num >= 1000) {
    return `${(num / 1000).toFixed(1)}K회`
  }
  return `${num.toLocaleString()}회`
}

const showToastMessage = (message, type = 'success') => {
  toastMessage.value = message
  toastType.value = type
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

const getToastIcon = () => {
  switch (toastType.value) {
    case 'success': return 'fa-check-circle'
    case 'error': return 'fa-exclamation-circle'
    case 'info': return 'fa-info-circle'
    default: return 'fa-check-circle'
  }
}

onMounted(async () => {
  await fetchVideoDetail()
  await fetchSummary()
  
  // 저장 상태 확인
  const saved = JSON.parse(localStorage.getItem('savedVideos') || '[]')
  isSaved.value = saved.includes(videoId)
  
  isLoading.value = false
})
</script>

<style scoped>
.video-detail-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

/* 네비게이션 헤더 */
.nav-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
  padding: 20px 24px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.back-btn {
  background: linear-gradient(135deg, #4DD0B1 0%, #3CBFA0 100%);
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 8px rgba(77, 208, 177, 0.3);
}

.back-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(77, 208, 177, 0.4);
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #6b7280;
}

.breadcrumb-item {
  color: #9ca3af;
}

.breadcrumb-current {
  color: #4DD0B1;
  font-weight: 600;
}

/* 로딩 상태 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
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

/* 메인 콘텐츠 */
.video-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 32px;
  animation: fadeInUp 0.6s ease-out;
}

/* 비디오 플레이어 섹션 */
.video-player-section {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.video-container {
  position: relative;
  width: 100%;
  height: 0;
  padding-bottom: 56.25%; /* 16:9 비율 */
  background: #000;
}

.video-iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none;
}

.video-info-section {
  padding: 32px;
}

.video-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 24px;
}

.video-title {
  flex: 1;
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
  line-height: 1.4;
}

.video-actions {
  display: flex;
  gap: 12px;
  flex-shrink: 0;
}

.action-btn {
  padding: 12px 20px;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
}

.save-btn {
  background: linear-gradient(135deg, #4DD0B1 0%, #3CBFA0 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(77, 208, 177, 0.3);
}

.save-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(77, 208, 177, 0.4);
}

.save-btn.saved {
  background: #f3f4f6;
  color: #6b7280;
  box-shadow: none;
}

.share-btn {
  background: #f8fafc;
  color: #6b7280;
  border: 1px solid #e5e7eb;
}

.share-btn:hover {
  background: #f1f5f9;
  border-color: #d1d5db;
}

.video-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #6b7280;
}

.meta-item i {
  color: #4DD0B1;
  width: 16px;
}

.channel-name {
  color: #1f2937;
  font-weight: 600;
}

/* 영상 설명 */
.video-description {
  border-top: 1px solid #e5e7eb;
  padding-top: 24px;
}

.description-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 16px 0;
}

.description-content {
  max-height: 150px;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.description-content.expanded {
  max-height: none;
}

.description-content p {
  font-size: 14px;
  color: #374151;
  line-height: 1.6;
  margin: 0;
  white-space: pre-wrap;
}

.toggle-description-btn {
  background: none;
  border: none;
  color: #4DD0B1;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 12px;
  padding: 0;
}

.toggle-description-btn:hover {
  color: #3CBFA0;
}

/* AI 요약 섹션 */
.ai-summary-section {
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
  border: 1px solid rgba(245, 158, 11, 0.3);
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 8px 32px rgba(245, 158, 11, 0.1);
}

.summary-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.ai-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: white;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.summary-title {
  flex: 1;
}

.summary-title h3 {
  font-size: 20px;
  font-weight: 700;
  color: #92400e;
  margin: 0 0 4px 0;
}

.ai-badge {
  background: rgba(245, 158, 11, 0.2);
  color: #92400e;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.retry-btn {
  background: rgba(245, 158, 11, 0.1);
  color: #92400e;
  border: 1px solid rgba(245, 158, 11, 0.3);
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.retry-btn:hover {
  background: rgba(245, 158, 11, 0.2);
}

.summary-content {
  min-height: 100px;
}

.summary-loading {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 0;
}

.summary-spinner {
  width: 24px;
  height: 24px;
  border: 3px solid rgba(146, 64, 14, 0.3);
  border-top: 3px solid #92400e;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.summary-loading p {
  font-size: 14px;
  color: #92400e;
  margin: 0;
}

.summary-result p {
  font-size: 15px;
  color: #92400e;
  line-height: 1.7;
  margin: 0 0 16px 0;
}

.summary-footer {
  padding-top: 16px;
  border-top: 1px solid rgba(245, 158, 11, 0.3);
}

.summary-note {
  font-size: 12px;
  color: rgba(146, 64, 14, 0.7);
  display: flex;
  align-items: center;
  gap: 6px;
}

.summary-error {
  text-align: center;
  padding: 40px 20px;
}

.error-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.summary-error h4 {
  font-size: 16px;
  color: #92400e;
  margin: 0 0 8px 0;
}

.summary-error p {
  font-size: 14px;
  color: rgba(146, 64, 14, 0.7);
  margin: 0;
}

/* 관련 영상 섹션 */
.related-videos-section {
  background: white;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 24px 0;
}

.related-videos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.related-video-card {
  display: flex;
  gap: 12px;
  padding: 12px;
  border-radius: 12px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.related-video-card:hover {
  background: #f8fafc;
}

.related-thumbnail {
  width: 80px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
  flex-shrink: 0;
}

.related-info {
  flex: 1;
  min-width: 0;
}

.related-title {
  font-size: 13px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 4px 0;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.related-channel {
  font-size: 11px;
  color: #6b7280;
  margin: 0;
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

.toast.info {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.toast.error {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
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
  .video-detail-page {
    padding: 20px 16px;
  }
  
  .nav-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .video-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .video-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .action-btn {
    flex: 1;
    justify-content: center;
  }
  
  .video-meta {
    flex-direction: column;
    gap: 12px;
  }
  
  .ai-summary-section,
  .video-info-section {
    padding: 20px;
  }
  
  .related-videos-grid {
    grid-template-columns: 1fr;
  }
}
</style>