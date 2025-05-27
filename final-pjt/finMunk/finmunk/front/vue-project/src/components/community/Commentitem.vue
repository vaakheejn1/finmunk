<!-- front/vue-project/src/components/CommentItem.vue -->
<template>
  <div class="comments-container">
    <TransitionGroup name="comment-list" tag="ul" class="comment-list">
      <li v-for="comment in comments" :key="comment.id" class="comment-item">
        <!-- 댓글 아바타 -->
        <div class="comment-avatar">
          <img
            v-if="comment.user && comment.user.profile_image"
            :src="comment.user.profile_image"
            alt="프로필 이미지"
            class="comment-avatar-img"
          />
          <span v-else class="avatar-icon">🐿️</span>
        </div>

        <div class="comment-content-wrapper">
          <!-- 댓글 헤더 -->
          <div class="comment-header">
            <strong 
              class="comment-author"
              @click.stop="$emit('show-profile', { id: comment.user.id, username: comment.user.username }, $event)"
            >
              {{ comment.user.username }}
              {{ logComment(comment) }}
            </strong>

            <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
          </div>

          <!-- 댓글 내용 -->
          <div class="comment-body">
            <!-- 수정 모드 -->
            <template v-if="editModeId === comment.id">
              <div class="edit-mode">
                <textarea 
                  v-model="editContent" 
                  @keydown.enter.prevent="handleEditEnter"
                  @keydown.esc="cancelEdit"
                  class="edit-input"
                  rows="2"
                  placeholder="댓글을 수정해주세요"
                  ref="editTextarea"
                />
                <div class="edit-actions">
                  <button @click="submitUpdate(comment.id)" class="edit-btn confirm">
                    <span>✅</span>
                    <span class="btn-text">저장</span>
                  </button>
                  <button @click="cancelEdit" class="edit-btn cancel">
                    <span>❌</span>
                    <span class="btn-text">취소</span>
                  </button>
                </div>
              </div>
            </template>

            <!-- 일반 모드 -->
            <template v-else>
              <p class="comment-text">{{ comment.content }}</p>

              <!-- 댓글 액션 버튼들 -->
              <div class="comment-actions">
                <!-- 좋아요 버튼 -->
                <button 
                  @click="toggleCommentLike(comment.id)" 
                  class="action-btn like-btn"
                  :class="{ 'liked': comment.is_liked }"
                >
                  <span class="like-icon">{{ comment.is_liked ? '❤️' : '🤍' }}</span>
                  <span class="like-count">{{ comment.like_count || 0 }}</span>
                </button>

                <!-- 멘션 버튼 -->
                <button 
                  @click="$emit('mention', comment.user)"
                  class="action-btn mention-btn"
                >
                  <span>@</span>
                  <span class="btn-text">답글</span>
                </button>

                <!-- 작성자 전용 버튼 -->
                <template v-if="isCommentOwner(comment.user)">
                  <button @click="startEdit(comment)" class="action-btn edit-btn">
                    <span>✏️</span>
                    <span class="btn-text">수정</span>
                  </button>
                  <button @click="deleteThisComment(comment.id)" class="action-btn delete-btn">
                    <span>🗑️</span>
                    <span class="btn-text">삭제</span>
                  </button>
                </template>
              </div>
            </template>
          </div>
        </div>

        <!-- 호버 시 나타나는 도토리 -->
        <div class="hover-acorn">🌰</div>
      </li>
    </TransitionGroup>

    <!-- 댓글이 없을 때 -->
    <div v-if="!comments || comments.length === 0" class="no-comments">
      <span class="no-comments-icon">💬</span>
      <p>아직 댓글이 없어요!</p>
      <p class="sub-text">첫 번째 댓글을 남겨보세요 🐿️</p>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { useUserStore } from '@/stores/user'
import { useCommunityStore } from '@/stores/community'
import axios from 'axios'

const props = defineProps({
  comments: Array,
  articleId: [String, Number]
})

const emit = defineEmits(['refresh', 'mention', 'show-profile'])

const userStore = useUserStore()
const communityStore = useCommunityStore()

const editModeId = ref(null)
const editContent = ref('')
const editTextarea = ref(null)

const logComment = (comment) => {
  console.log('💬 comment:', comment)
  return ''
}


// 시간 포맷팅
const formatTime = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) {
    return '방금 전'
  } else if (diff < 3600000) {
    const minutes = Math.floor(diff / 60000)
    return `${minutes}분 전`
  } else if (diff < 86400000) {
    const hours = Math.floor(diff / 3600000)
    return `${hours}시간 전`
  } else if (diff < 604800000) {
    const days = Math.floor(diff / 86400000)
    return `${days}일 전`
  } else {
    return date.toLocaleDateString('ko-KR')
  }
}

// 댓글 작성자 확인
const isCommentOwner = (commentUser) => {
  return userStore.user && commentUser === (userStore.user.username || userStore.user)
}

// 게시글 작성자인지 확인 (추가 기능)
const isArticleAuthor = (commentUser) => {
  // 실제 구현시 게시글 작성자 정보와 비교
  return false
}

// 댓글 좋아요 토글
const toggleCommentLike = (commentId) => {
  axios.post(`${import.meta.env.VITE_API_URL}/community/comments/${commentId}/like/`, {}, {
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  })
  .then(() => {
    emit('refresh')
  })
  .catch((err) => {
    alert('로그인이 필요해요! 🐿️')
    console.error(err)
  })
}

// 수정 모드 진입
const startEdit = (comment) => {
  editModeId.value = comment.id
  editContent.value = comment.content
  nextTick(() => {
    editTextarea.value?.focus()
  })
}

// 수정 취소
const cancelEdit = () => {
  editModeId.value = null
  editContent.value = ''
}

// 수정 엔터키 처리
const handleEditEnter = (e) => {
  if (!e.shiftKey && editModeId.value) {
    submitUpdate(editModeId.value)
  }
}

// 수정 제출
const submitUpdate = (commentId) => {
  if (!editContent.value.trim()) {
    alert('댓글을 입력해주세요 🐿️')
    return
  }

  communityStore.updateComment(
    commentId,
    props.articleId,
    editContent.value,
    () => {
      editModeId.value = null
      editContent.value = ''
      emit('refresh')
    }
  )
}

// 댓글 삭제
const deleteThisComment = (commentId) => {
  if (confirm('정말 이 댓글을 삭제할까요? 🗑️')) {
    communityStore.deleteComment(commentId, () => {
      emit('refresh')
    })
  }
}
</script>

<style scoped>
.comments-container {
  margin-top: 20px;
}

.comment-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 댓글 아이템 */
.comment-item {
  display: flex;
  gap: 15px;
  padding: 20px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.comment-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

/* 아바타 */
.comment-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.comment-avatar-img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-icon {
  font-size: 1.3rem;
}

/* 댓글 내용 */
.comment-content-wrapper {
  flex: 1;
  min-width: 0;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.comment-author {
  font-weight: 600;
  color: #333;
  cursor: pointer;
  transition: color 0.3s;
  display: flex;
  align-items: center;
  gap: 5px;
}

.comment-author:hover {
  color: #4CAF50;
}

.author-badge {
  font-size: 0.9rem;
  background: #ffeaa7;
  padding: 2px 6px;
  border-radius: 10px;
}

.comment-time {
  font-size: 0.85rem;
  color: #999;
  margin-left: auto;
}

.comment-body {
  position: relative;
}

.comment-text {
  color: #555;
  line-height: 1.6;
  margin: 0 0 10px 0;
  word-break: keep-all;
}

/* 댓글 액션 버튼들 */
.comment-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.action-btn {
  padding: 5px 12px;
  background: #f8f8f8;
  border: 1px solid #e0e0e0;
  border-radius: 15px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 5px;
}

.action-btn:hover {
  background: #f0f0f0;
  transform: translateY(-1px);
}

.like-btn.liked {
  background: #fff5f5;
  border-color: #ff4757;
  color: #ff4757;
}

.like-icon {
  font-size: 1rem;
}

.mention-btn:hover {
  background: #e3f2fd;
  border-color: #2196f3;
  color: #2196f3;
}

.edit-btn:hover {
  background: #e8f5e9;
  border-color: #4CAF50;
  color: #4CAF50;
}

.delete-btn:hover {
  background: #ffebee;
  border-color: #f44336;
  color: #f44336;
}

.btn-text {
  font-size: 0.85rem;
}

/* 수정 모드 */
.edit-mode {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.edit-input {
  width: 100%;
  padding: 10px 15px;
  border: 2px solid #4CAF50;
  border-radius: 15px;
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
  min-height: 60px;
  background: #f8fff8;
  transition: all 0.3s;
}

.edit-input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.edit-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.edit-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 5px;
}

.edit-btn.confirm {
  background: #4CAF50;
  color: white;
}

.edit-btn.confirm:hover {
  background: #45a049;
  transform: translateY(-2px);
}

.edit-btn.cancel {
  background: #f44336;
  color: white;
}

.edit-btn.cancel:hover {
  background: #da190b;
  transform: translateY(-2px);
}

/* 호버 도토리 */
.hover-acorn {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 1.5rem;
  opacity: 0;
  transform: rotate(-15deg);
  transition: all 0.3s;
}

.comment-item:hover .hover-acorn {
  opacity: 0.2;
  transform: rotate(15deg);
}

/* 댓글 없음 */
.no-comments {
  text-align: center;
  padding: 60px 20px;
  background: #f8f8f8;
  border-radius: 20px;
  animation: fadeIn 0.5s ease-out;
}

.no-comments-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 15px;
  opacity: 0.5;
}

.no-comments p {
  color: #666;
  margin: 5px 0;
}

.sub-text {
  font-size: 0.9rem;
  color: #999;
}

/* 트랜지션 */
.comment-list-enter-active,
.comment-list-leave-active {
  transition: all 0.3s ease;
}

.comment-list-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.comment-list-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

/* 반응형 */
@media (max-width: 768px) {
  .comment-item {
    padding: 15px;
  }

  .comment-avatar {
    width: 35px;
    height: 35px;
  }

  .comment-header {
    flex-wrap: wrap;
  }

  .comment-time {
    width: 100%;
    margin-left: 0;
    margin-top: 5px;
  }

  .comment-actions {
    flex-wrap: wrap;
  }

  .action-btn {
    padding: 4px 10px;
    font-size: 0.8rem;
  }

  .btn-text {
    display: none;
  }

  .edit-actions {
    width: 100%;
  }

  .edit-btn {
    flex: 1;
    justify-content: center;
  }
}

/* 다크 모드 */
@media (prefers-color-scheme: dark) {
  .comment-item {
    background: #2a2a2a;
  }

  .comment-author {
    color: #f0f0f0;
  }

  .comment-author:hover {
    color: #4CAF50;
  }

  .comment-text {
    color: #d0d0d0;
  }

  .action-btn {
    background: #333;
    border-color: #444;
    color: #f0f0f0;
  }

  .action-btn:hover {
    background: #444;
  }

  .edit-input {
    background: #333;
    border-color: #4CAF50;
    color: #f0f0f0;
  }

  .no-comments {
    background: #2a2a2a;
  }

  .no-comments p {
    color: #d0d0d0;
  }
}
</style>