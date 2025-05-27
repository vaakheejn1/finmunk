<template>
  <div class="saved-videos-page">
    <!-- 페이지 헤더 -->
    <div class="page-header">
      <div class="header-icon">
        <i class="fas fa-bookmark"></i>
      </div>
      <div class="header-content">
        <h2 class="page-title">💾 저장된 영상</h2>
        <p class="page-subtitle">나중에 볼 영상들을 관리하세요</p>
      </div>
      <div class="video-count">
        <span class="count-number">{{ videos.length }}</span>
        <span class="count-text">개 영상</span>
      </div>
    </div>

    <!-- 메인 콘텐츠 -->
    <div class="videos-container">
      <!-- 빈 상태 -->
      <div v-if="videos.length === 0" class="empty-state">
        <div class="empty-icon">📺</div>
        <h3 class="empty-title">저장된 영상이 없습니다</h3>
        <p class="empty-description">관심 있는 영상을 저장하여 나중에 편리하게 시청하세요</p>
        <button class="browse-btn" @click="$router.push('/videos')">
          <i class="fas fa-search"></i>
          영상 둘러보기
        </button>
      </div>

      <!-- 영상 목록 -->
      <div v-else class="videos-grid">
        <div 
          v-for="(video, index) in videos" 
          :key="video.id.videoId"
          class="video-card"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <!-- 썸네일 영역 -->
          <div class="video-thumbnail">
            <iframe
              :src="`https://www.youtube.com/embed/${video.id.videoId}`"
              frameborder="0"
              allowfullscreen
              class="video-iframe"
            ></iframe>
            <div class="video-overlay">
              <button class="play-btn">
                <i class="fas fa-play"></i>
              </button>
            </div>
          </div>

          <!-- 영상 정보 -->
          <div class="video-info">
            <h3 class="video-title">{{ video.snippet.title }}</h3>
            <div class="video-meta">
              <span class="channel-name">{{ video.snippet.channelTitle }}</span>
              <span class="publish-date">{{ formatDate(video.snippet.publishedAt) }}</span>
            </div>
            <p class="video-description">{{ truncateDescription(video.snippet.description) }}</p>
          </div>

          <!-- 액션 버튼들 -->
          <div class="video-actions">
            <button class="action-btn watch-btn" @click="watchVideo(video.id.videoId)">
              <i class="fas fa-play"></i>
              시청하기
            </button>
            <button class="action-btn remove-btn" @click="removeVideo(video.id.videoId)">
              <i class="fas fa-trash"></i>
              삭제
            </button>
          </div>

          <!-- 저장 날짜 -->
          <div class="saved-date">
            <i class="fas fa-clock"></i>
            저장됨: {{ formatSavedDate(video.savedAt) }}
          </div>
        </div>
      </div>
    </div>

    <!-- 삭제 확인 모달 -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="cancelDelete">
      <div class="delete-modal" @click.stop>
        <div class="modal-icon">
          <i class="fas fa-exclamation-triangle"></i>
        </div>
        <h3 class="modal-title">영상을 삭제하시겠습니까?</h3>
        <p class="modal-description">이 작업은 되돌릴 수 없습니다.</p>
        <div class="modal-actions">
          <button class="modal-btn cancel-btn" @click="cancelDelete">취소</button>
          <button class="modal-btn confirm-btn" @click="confirmDelete">삭제</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const videos = ref([])
const showDeleteModal = ref(false)
const videoToDelete = ref(null)

const loadSavedVideos = () => {
  const saved = JSON.parse(localStorage.getItem('watchLater') || '[]')
  videos.value = saved
}

onMounted(() => {
  loadSavedVideos()
})

const removeVideo = (videoId) => {
  videoToDelete.value = videoId
  showDeleteModal.value = true
}

const confirmDelete = () => {
  videos.value = videos.value.filter(v => v.id.videoId !== videoToDelete.value)
  localStorage.setItem('watchLater', JSON.stringify(videos.value))
  showDeleteModal.value = false
  videoToDelete.value = null
}

const cancelDelete = () => {
  showDeleteModal.value = false
  videoToDelete.value = null
}

const watchVideo = (videoId) => {
  window.open(`https://www.youtube.com/watch?v=${videoId}`, '_blank')
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const formatSavedDate = (dateString) => {
  if (!dateString) return '최근'
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR')
}

const truncateDescription = (description) => {
  if (!description) return ''
  return description.length > 100 ? description.substring(0, 100) + '...' : description
}

onMounted(() => {
  loadSavedVideos()
})
</script>

<style scoped>
.saved-videos-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

/* 페이지 헤더 */
.page-header {
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

.video-count {
  text-align: center;
  background: rgba(255, 255, 255, 0.2);
  padding: 16px 20px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.count-number {
  display: block;
  font-size: 24px;
  font-weight: 700;
}

.count-text {
  font-size: 12px;
  opacity: 0.8;
}

/* 메인 콘텐츠 */
.videos-container {
  animation: fadeInUp 0.6s ease-out;
}

/* 빈 상태 */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 24px;
}

.empty-title {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 12px 0;
}

.empty-description {
  font-size: 16px;
  color: #6b7280;
  margin: 0 0 32px 0;
  line-height: 1.6;
}

.browse-btn {
  background: linear-gradient(135deg, #4DD0B1 0%, #3CBFA0 100%);
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 16px rgba(77, 208, 177, 0.3);
}

.browse-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(77, 208, 177, 0.4);
}

/* 영상 그리드 */
.videos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.video-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  animation: fadeInUp 0.6s ease-out both;
  position: relative;
}

.video-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

/* 썸네일 */
.video-thumbnail {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.video-iframe {
  width: 100%;
  height: 100%;
  border: none;
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.3) 0%, rgba(0, 0, 0, 0.1) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.video-card:hover .video-overlay {
  opacity: 1;
}

.play-btn {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50%;
  font-size: 20px;
  color: #4DD0B1;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.play-btn:hover {
  transform: scale(1.1);
  background: white;
}

/* 영상 정보 */
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
}

/* 액션 버튼 */
.video-actions {
  display: flex;
  gap: 8px;
  padding: 0 20px 20px;
}

.action-btn {
  flex: 1;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.watch-btn {
  background: linear-gradient(135deg, #4DD0B1 0%, #3CBFA0 100%);
  color: white;
}

.watch-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(77, 208, 177, 0.3);
}

.remove-btn {
  background: #f8fafc;
  color: #ef4444;
  border: 1px solid #fee2e2;
}

.remove-btn:hover {
  background: #fef2f2;
  border-color: #fecaca;
}

/* 저장 날짜 */
.saved-date {
  padding: 0 20px 16px;
  font-size: 11px;
  color: #9ca3af;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* 삭제 모달 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

.delete-modal {
  background: white;
  border-radius: 20px;
  padding: 32px;
  max-width: 400px;
  width: 90%;
  text-align: center;
  animation: scaleIn 0.3s ease-out;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #f59e0b;
  margin: 0 auto 20px;
}

.modal-title {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.modal-description {
  font-size: 14px;
  color: #6b7280;
  margin: 0 0 24px 0;
}

.modal-actions {
  display: flex;
  gap: 12px;
}

.modal-btn {
  flex: 1;
  padding: 12px 24px;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn {
  background: #f8fafc;
  color: #6b7280;
  border: 1px solid #e5e7eb;
}

.cancel-btn:hover {
  background: #f1f5f9;
}

.confirm-btn {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.confirm-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
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

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .saved-videos-page {
    padding: 20px 16px;
  }
  
  .page-header {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
  
  .videos-grid {
    grid-template-columns: 1fr;
  }
  
  .video-card {
    margin: 0;
  }
  
  .video-actions {
    flex-direction: column;
  }
}
</style>