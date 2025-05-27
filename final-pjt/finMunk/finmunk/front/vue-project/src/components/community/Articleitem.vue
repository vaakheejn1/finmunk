<template>
  <div class="article-card" @click="goToDetail">
    <!-- 카테고리 배지 -->
    <div class="category-badge" :class="`category-${article.category}`">
      <span class="category-icon">{{ getCategoryIcon(article.category) }}</span>
      <span class="category-text">{{ getCategoryName(article.category) }}</span>
    </div>

    <!-- 메인 콘텐츠 -->
    <div class="card-content">
      <h3 class="article-title">
        <span class="title-text">{{ article.title }}</span>
        <span v-if="article.image" class="image-indicator">🖼️</span>
      </h3>
      
      <!-- 미리보기 텍스트 -->
      <p v-if="article.content" class="article-preview">
        {{ truncateText(article.content, 100) }}
      </p>

      <!-- 메타 정보 -->
      <div class="article-meta">
        <div class="meta-left">
          <span class="author-info">
            <img
            v-if="article.user && article.user.profile_image"
            :src="article.user.profile_image"
            alt="프로필"
            class="author-img"
          />
          <span v-else class="author-fallback">🐿️</span>
            
            <span 
              class="author-name"
              @click.stop="$emit('show-profile', { id: article.user.id, username: article.user.username }, $event)"
            >
              @{{ article.user.username }}
            </span>

          </span>
          <span class="meta-divider">•</span>
          <span class="time-info">
            <span class="time-icon">🕒</span>
            <span class="time-text">{{ formatDate(article.created_at) }}</span>
          </span>
        </div>
        
        <div class="meta-right">
          <span class="comment-info">
            <span class="comment-icon">💬</span>
            <span class="comment-count">{{ article.comment_count || 0 }}</span>
          </span>
          <span class="like-info" v-if="article.like_count !== undefined">
            <span class="like-icon">❤️</span>
            <span class="like-count">{{ article.like_count || 0 }}</span>
          </span>
        </div>
      </div>
    </div>

    <!-- 호버 효과 장식 -->
    <div class="hover-decoration">
      <span class="hover-acorn">🌰</span>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const emit = defineEmits(['show-profile'])

const props = defineProps({ 
  article: Object 
})

const router = useRouter()

const goToDetail = () => {
  router.push({ name: 'CommunityArticle', params: { id: props.article.id } })
}

// 카테고리별 아이콘
const getCategoryIcon = (category) => {
  const icons = {
    notice: '📢',
    event: '🎉',
    tip: '💡'
  }
  return icons[category] || '📝'
}

// 카테고리별 이름
const getCategoryName = (category) => {
  const names = {
    notice: '공지',
    event: '이벤트',
    tip: '자유'
  }
  return names[category] || '일반'
}

// 텍스트 자르기
const truncateText = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.slice(0, length) + '...' : text
}

// 날짜 포맷팅
const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  
  // 1분 이내
  if (diff < 60000) {
    return '방금 전'
  }
  // 1시간 이내
  else if (diff < 3600000) {
    const minutes = Math.floor(diff / 60000)
    return `${minutes}분 전`
  }
  // 24시간 이내
  else if (diff < 86400000) {
    const hours = Math.floor(diff / 3600000)
    return `${hours}시간 전`
  }
  // 7일 이내
  else if (diff < 604800000) {
    const days = Math.floor(diff / 86400000)
    return `${days}일 전`
  }
  // 그 외
  else {
    return date.toLocaleDateString('ko-KR', {
      month: 'long',
      day: 'numeric'
    })
  }
}
</script>

<style scoped>
.article-card {
  background: white;
  border-radius: 20px;
  padding: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.06);
  border: 2px solid transparent;
}

.article-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border-color: #4CAF50;
}

/* 카테고리 배지 */
.category-badge {
  position: absolute;
  top: 15px;
  right: 15px;
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 12px;
  border-radius: 15px;
  font-size: 0.85rem;
  font-weight: 600;
}

.category-notice {
  background: #fff3cd;
  color: #856404;
}

.category-event {
  background: #f8d7da;
  color: #721c24;
}

.category-tip {
  background: #d1ecf1;
  color: #0c5460;
}

.category-icon {
  font-size: 1rem;
}

/* 메인 콘텐츠 */
.card-content {
  position: relative;
  z-index: 1;
}

.article-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 12px 0;
  display: flex;
  align-items: center;
  gap: 8px;
  line-height: 1.4;
  padding-right: 100px; /* 카테고리 배지 공간 확보 */
}

.title-text {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.image-indicator {
  font-size: 1.1rem;
  opacity: 0.7;
  flex-shrink: 0;
}

.author-img {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  object-fit: cover;
}

.article-preview {
  color: #666;
  line-height: 1.6;
  margin: 0 0 15px 0;
  font-size: 0.95rem;
}

/* 메타 정보 */
.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  color: #999;
  gap: 15px;
}

.meta-left {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  min-width: 0;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 6px;
}

.author-avatar {
  width: 24px;
  height: 24px;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}

.author-name {
  font-weight: 600;
  color: #555;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.meta-divider {
  color: #ddd;
}

.time-info {
  display: flex;
  align-items: center;
  gap: 4px;
}

.time-icon {
  font-size: 0.9rem;
}

.time-text {
  white-space: nowrap;
}

.meta-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.comment-info,
.like-info {
  display: flex;
  align-items: center;
  gap: 5px;
}

.comment-icon,
.like-icon {
  font-size: 1rem;
}

.comment-count,
.like-count {
  font-weight: 600;
  color: #666;
}

/* 호버 효과 */
.hover-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s;
}

.article-card:hover .hover-decoration {
  opacity: 1;
}

.hover-acorn {
  position: absolute;
  bottom: 10px;
  left: 10px;
  font-size: 2.5rem;
  opacity: 0.1;
  animation: rotateAcorn 0.6s ease-out;
}

@keyframes rotateAcorn {
  from {
    transform: rotate(0deg) scale(0.8);
  }
  to {
    transform: rotate(360deg) scale(1);
  }
}

/* 모바일 반응형 */
@media (max-width: 768px) {
  .article-card {
    padding: 20px;
  }

  .article-title {
    font-size: 1.1rem;
    padding-right: 80px;
  }

  .category-badge {
    padding: 4px 10px;
    font-size: 0.8rem;
  }

  .article-preview {
    font-size: 0.9rem;
  }

  .article-meta {
    font-size: 0.85rem;
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .meta-left {
    width: 100%;
  }

  .meta-right {
    width: 100%;
    justify-content: flex-start;
  }

  .author-name {
    max-width: 100px;
  }
}

/* 다크 모드 */
@media (prefers-color-scheme: dark) {
  .article-card {
    background: #2a2a2a;
    border-color: #333;
  }

  .article-card:hover {
    border-color: #4CAF50;
  }

  .article-title {
    color: #f0f0f0;
  }

  .article-preview {
    color: #b0b0b0;
  }

  .author-name {
    color: #d0d0d0;
  }

  .comment-count,
  .like-count {
    color: #b0b0b0;
  }

  .meta-divider {
    color: #555;
  }
}

/* 애니메이션 */
.article-card {
  animation: fadeInUp 0.5s ease-out backwards;
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
</style>