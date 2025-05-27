<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCommunityStore } from '@/stores/community'
import { useUserStore } from '@/stores/user'
import CommentItem from '@/components/community/Commentitem.vue'
import CommentForm from '@/components/community/CommentForm.vue'
import UserProfileModal from '@/components/community/UserProfileModal.vue'
import Chatbot from '@/components/chatbot/Chatbot.vue'
import axios from 'axios'

const communityStore = useCommunityStore()
const userStore = useUserStore()
const route = useRoute()
const router = useRouter()
const showFullImage = ref(false)
const selectedUserId = ref(null)


const openUserProfile = (userId) => {
  console.log(`프로필 열기 - 유저 ID: ${userId}`)
  selectedUserId.value = userId
  showUserOption.value = false
}


const showUserOption = ref(false)
const selectedUser = ref(null)
const optionPopupPosition = ref({ x: 0, y: 0 })

const articleId = route.params.id
const mentionText = ref('') // 🆕 언급 텍스트

const handleUserClick = (user, event) => {
  selectedUser.value = user
  showUserOption.value = true
  optionPopupPosition.value = {
    x: event.clientX,
    y: event.clientY
  }
}

const reloadComments = function () {
  communityStore.loadComments(articleId)
}

onMounted(() => {
  communityStore.loadArticle(articleId)
  communityStore.loadComments(articleId)
})

const deleteArticle = function () {
  if (confirm('정말 삭제하시겠습니까?')) {
    communityStore.deleteArticle(articleId, function () {
      alert('삭제 완료!')
      router.push({ name: 'Community' })
    })
  }
}

const toggleLike = () => {
  axios.post(`${import.meta.env.VITE_API_URL}/community/articles/${articleId}/like/`, {}, {
    headers: { Authorization: `Token ${userStore.token}` }
  })
  .then(res => {
    communityStore.selectedArticle.like_count = res.data.like_count
    communityStore.selectedArticle.is_liked = res.data.liked
  })
  .catch(err => {
    alert('로그인이 필요해요!')
    console.error(err)
  })
}

// 🆕 댓글에서 유저 클릭 시 호출될 함수
const handleMention = (username) => {
  mentionText.value = `@${username}`
}
</script>

<template>
  <div class="article-container">
    <!-- 배경 장식 -->
    <div class="bg-decoration">
      <span class="deco-item" v-for="n in 8" :key="n">🌰</span>
    </div>

    <!-- 게시글 카드 -->
    <article class="article-card">
      <!-- 헤더 섹션 -->
      <div class="article-header">
        <h1 class="article-title">
          <span class="title-icon bounce">📝</span>
          {{ communityStore.selectedArticle?.title }}
        </h1>
        
        <div class="article-meta">
          <div class="author-info">
            <img
              v-if="communityStore.selectedArticle?.user?.profile_image"
              :src="communityStore.selectedArticle.user.profile_image"
              alt="프로필 이미지"
              class="author-avatar-img"
            />
            <span v-else class="author-avatar">🐿️</span>
            <span
              class="author-name"
              v-if="communityStore.selectedArticle?.user"
              @click="handleUserClick(communityStore.selectedArticle.user, $event)"
              style="cursor: pointer;"
            >
              @{{ communityStore.selectedArticle.user.username }}
            </span>
          </div>
          <div class="meta-right">
            <span class="date">{{ new Date(communityStore.selectedArticle?.created_at).toLocaleDateString() }}</span>
          </div>
        </div>
      </div>

      <!-- 이미지 섹션 -->
      <div v-if="communityStore.selectedArticle?.image" class="image-section">
        <img
          :src="communityStore.selectedArticle.image"
          alt="게시글 이미지"
          class="article-image"
          @click="showFullImage = true"
        />
        <div class="image-overlay">
          <span class="overlay-icon">🖼️</span>
        </div>
      </div>

      <!-- 이미지 클릭 시 열리는 모달 -->
      <div v-if="showFullImage" class="modal" @click.self="showFullImage = false">
        <img :src="communityStore.selectedArticle.image" class="modal-image" />
      </div>

      <!-- 본문 섹션 -->
      <div class="article-content">
        <p>{{ communityStore.selectedArticle?.content }}</p>
      </div>

      <!-- 액션 버튼들 -->
      <div class="article-actions">
        <button 
          @click="toggleLike" 
          class="like-btn"
          :class="{ 'liked': communityStore.selectedArticle?.is_liked }"
        >
          <span class="like-icon">{{ communityStore.selectedArticle?.is_liked ? '❤️' : '🤍' }}</span>
          <span class="like-count">{{ communityStore.selectedArticle?.like_count || 0 }}</span>
          <span class="like-text">{{ communityStore.selectedArticle?.is_liked ? '좋아요 취소' : '좋아요' }}</span>
        </button>

        <div v-if="userStore.user && communityStore.selectedArticle?.user === userStore.user.username" class="owner-actions">
          <RouterLink :to="{ name: 'CommunityWrite', query: { id: communityStore.selectedArticle.id } }">
            <button class="edit-btn">
              <span>✏️</span>
              수정
            </button>
          </RouterLink>
          <button @click="deleteArticle" class="delete-btn">
            <span>🗑️</span>
            삭제
          </button>
        </div>
      </div>
    </article>

    <!-- 댓글 섹션 -->
    <section class="comment-section">
      <h2 class="section-title">
        <span class="title-icon wiggle">💬</span>
        댓글
        <span class="comment-count">{{ communityStore.comments?.length || 0 }}개</span>
      </h2>

      <!-- 댓글 작성 폼 -->
      <div class="comment-form-wrapper">
        <CommentForm
          :articleId="Number(articleId)"
          :mentionText="mentionText"
          @refresh="reloadComments"
        />
      </div>

      <!-- 댓글 목록 -->
      <div class="comments-list">
        <CommentItem
          :comments="communityStore.comments"
          :articleId="Number(articleId)"
          @refresh="reloadComments"
          @mention="handleMention"
          @show-profile="(userId, event) => handleUserClick(userId, event)"
        />
      </div>
    </section>
  </div>

  <div
    v-if="showUserOption && selectedUser"
    class="user-popup"
    :style="`top: ${optionPopupPosition.y}px; left: ${optionPopupPosition.x}px;`"
  >
    <p>@{{ selectedUser.username }}</p>
    <button @click="mentionText = '@' + selectedUser.username; showUserOption = false">💬 언급하기</button>
    <button @click="openUserProfile(selectedUser.id)">👤 프로필 보기</button>
  </div>

  <UserProfileModal
    v-if="selectedUserId"
    :userId="selectedUserId"
    :show="true"
    @close="selectedUserId = null"
  />

<Chatbot/>
</template>

<style scoped>
/* 기본 컨테이너 */
.article-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  position: relative;
}

.author-avatar-img {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #ddd;
}

/* 배경 장식 */
.bg-decoration {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: -1;
  overflow: hidden;
}

.deco-item {
  position: absolute;
  font-size: 2rem;
  opacity: 0.1;
  animation: float 15s infinite linear;
}

.deco-item:nth-child(1) { top: 10%; left: 5%; animation-delay: 0s; }
.deco-item:nth-child(2) { top: 20%; left: 85%; animation-delay: 2s; }
.deco-item:nth-child(3) { top: 40%; left: 15%; animation-delay: 4s; }
.deco-item:nth-child(4) { top: 60%; left: 75%; animation-delay: 6s; }
.deco-item:nth-child(5) { top: 80%; left: 25%; animation-delay: 8s; }
.deco-item:nth-child(6) { top: 30%; left: 45%; animation-delay: 10s; }
.deco-item:nth-child(7) { top: 70%; left: 55%; animation-delay: 12s; }
.deco-item:nth-child(8) { top: 50%; left: 95%; animation-delay: 14s; }

@keyframes float {
  0% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(180deg); }
  100% { transform: translateY(0) rotate(360deg); }
}

/* 게시글 카드 */
.article-card {
  background: white;
  border-radius: 30px;
  padding: 40px;
  margin-bottom: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  animation: slideIn 0.6s ease-out;
  position: relative;
  overflow: hidden;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 헤더 섹션 */
.article-header {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f0f0f0;
}

.article-title {
  font-size: 2rem;
  color: #2c3e50;
  margin: 0 0 20px 0;
  display: flex;
  align-items: center;
  gap: 15px;
  line-height: 1.4;
}

.title-icon {
  font-size: 1.8rem;
  display: inline-block;
  flex-shrink: 0;
}

.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #666;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.author-avatar {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.author-name {
  font-weight: 600;
  color: #333;
}

.date {
  font-size: 0.9rem;
  color: #999;
}

/* 이미지 섹션 */
.image-section {
  margin: 20px -40px;
  position: relative;
  overflow: hidden;
  border-radius: 20px;
}

.article-image {
  max-width: 100%;
  max-height: 400px;   
  object-fit: contain; 
  display: block;
  margin: 0 auto;
  cursor: pointer;   
}

.image-section:hover .article-image {
  transform: scale(1.05);
}

.image-overlay {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(255, 255, 255, 0.9);
  padding: 10px 15px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  gap: 5px;
  opacity: 0;
  transition: opacity 0.3s;
}

.image-section:hover .image-overlay {
  opacity: 1;
}

/* 본문 섹션 */
.article-content {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #333;
  margin: 30px 0;
  word-break: keep-all;
}

/* 액션 버튼들 */
.article-actions {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 2px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.like-btn {
  background: #f8f8f8;
  border: 2px solid #e0e0e0;
  padding: 12px 24px;
  border-radius: 25px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.like-btn:hover {
  background: #fff;
  border-color: #ff4757;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 71, 87, 0.2);
}

.like-btn.liked {
  background: #fff5f5;
  border-color: #ff4757;
  color: #ff4757;
}

.like-icon {
  font-size: 1.3rem;
  transition: transform 0.3s;
}

.like-btn:hover .like-icon {
  transform: scale(1.2);
}

.like-btn.liked .like-icon {
  animation: heartBeat 0.6s;
}

@keyframes heartBeat {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.3); }
}

.like-count {
  font-weight: 700;
}

.owner-actions {
  display: flex;
  gap: 10px;
}

.edit-btn,
.delete-btn {
  padding: 10px 20px;
  border-radius: 20px;
  border: none;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s;
}

.edit-btn {
  background: #4CAF50;
  color: white;
}

.edit-btn:hover {
  background: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
}

.delete-btn {
  background: #ff4757;
  color: white;
}

.delete-btn:hover {
  background: #ff3838;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 71, 87, 0.3);
}

/* 댓글 섹션 */
.comment-section {
  background: white;
  border-radius: 30px;
  padding: 40px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  animation: slideIn 0.6s ease-out 0.2s backwards;
}

.section-title {
  font-size: 1.6rem;
  color: #2c3e50;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.comment-count {
  font-size: 1rem;
  color: #666;
  background: #f0f0f0;
  padding: 5px 15px;
  border-radius: 20px;
  margin-left: auto;
}

.comment-form-wrapper {
  background: #f8f8f8;
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 30px;
  border: 2px solid #e0e0e0;
  transition: all 0.3s;
}

.comment-form-wrapper:focus-within {
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* 플로팅 버튼 */
.floating-buttons {
  position: fixed;
  bottom: 30px;
  right: 30px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  z-index: 100;
}

.floating-btn {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: white;
  border: 2px solid #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  text-decoration: none;
  color: inherit;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.floating-btn:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.back-btn {
  background: #4CAF50;
  border-color: #4CAF50;
}

.top-btn {
  background: #ff9800;
  border-color: #ff9800;
}

.tooltip {
  position: absolute;
  right: 100%;
  top: 50%;
  transform: translateY(-50%);
  background: #333;
  color: white;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 0.9rem;
  white-space: nowrap;
  margin-right: 10px;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s;
}

.tooltip::after {
  content: '';
  position: absolute;
  left: 100%;
  top: 50%;
  transform: translateY(-50%);
  border: 5px solid transparent;
  border-left-color: #333;
}

.floating-btn:hover .tooltip {
  opacity: 1;
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
  .article-container {
    padding: 10px;
  }

  .article-card,
  .comment-section {
    padding: 25px 20px;
    border-radius: 20px;
  }

  .article-title {
    font-size: 1.5rem;
  }

  .article-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .image-section {
    margin: 20px -20px;
  }

  .article-actions {
    flex-direction: column;
    gap: 15px;
  }

  .like-btn {
    width: 100%;
    justify-content: center;
  }

  .owner-actions {
    width: 100%;
  }

  .owner-actions a,
  .owner-actions button {
    flex: 1;
  }

  .floating-buttons {
    bottom: 20px;
    right: 20px;
  }

  .floating-btn {
    width: 50px;
    height: 50px;
    font-size: 1.3rem;
  }
}

/* 다크 모드 지원 */
@media (prefers-color-scheme: dark) {
  .article-card,
  .comment-section {
    background: #2a2a2a;
    color: #f0f0f0;
  }

  .article-title,
  .section-title {
    color: #f0f0f0;
  }

  .article-content {
    color: #e0e0e0;
  }

  .article-header,
  .article-actions {
    border-color: #444;
  }

  .like-btn {
    background: #333;
    border-color: #444;
    color: #f0f0f0;
  }

  .like-btn:hover {
    background: #444;
    border-color: #ff4757;
  }

  .comment-form-wrapper {
    background: #333;
    border-color: #444;
  }

  .floating-btn {
    background: #333;
    border-color: #444;
  }
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-image {
  max-width: 90vw;
  max-height: 90vh;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
}

.user-popup {
  position: fixed;
  background: white;
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 12px;
  box-shadow: 0 3px 10px rgba(0,0,0,0.1);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 8px;
  animation: fadeIn 0.2s ease-out;
}


</style>