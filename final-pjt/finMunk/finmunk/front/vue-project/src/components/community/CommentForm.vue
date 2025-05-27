<template>
  <div class="comment-form-container">
    <!-- 로그인한 사용자 -->
    <div v-if="userStore.user" class="comment-form-wrapper">
      <div class="user-avatar">
        <span class="avatar-icon">🐿️</span>
      </div>
      
      <div class="comment-input-area">
        <div class="input-wrapper">
          <textarea
            v-model="newComment"
            :placeholder="getPlaceholder()"
            @keydown.enter.prevent="handleEnterKey"
            @input="adjustTextareaHeight"
            ref="commentTextarea"
            class="comment-input"
            rows="1"
          />
          
          <!-- 입력 중 표시 -->
          <div v-if="newComment.length > 0" class="input-indicator">
            <span class="char-count" :class="{ 'warn': newComment.length > 500 }">
              {{ newComment.length }}/500
            </span>
          </div>
        </div>
        
        <div class="form-actions">
          <div class="action-buttons">
            <!-- 이모지 버튼 -->
            <button type="button" class="emoji-btn" @click="toggleEmojiPicker">
              <span>😊</span>
              <span class="tooltip">이모지</span>
            </button>
            
            <!-- 도토리 버튼 (재미 요소) -->
            <button type="button" class="acorn-btn" @click="addAcorn">
              <span>🌰</span>
              <span class="tooltip">도토리 추가</span>
            </button>
          </div>
          
          <button 
            @click="submitComment" 
            class="submit-btn"
            :disabled="!newComment.trim() || newComment.length > 500"
          >
            <span class="btn-icon">✏️</span>
            <span class="btn-text">등록</span>
          </button>
        </div>
        
        <!-- 이모지 피커 (간단한 버전) -->
        <div v-if="showEmojiPicker" class="emoji-picker">
          <span 
            v-for="emoji in emojis" 
            :key="emoji"
            @click="insertEmoji(emoji)"
            class="emoji-item"
          >
            {{ emoji }}
          </span>
        </div>
      </div>
    </div>

    <!-- 비로그인 사용자 -->
    <div v-else class="login-prompt">
      <div class="prompt-icon">
        <span class="sleeping-squirrel">😴</span>
      </div>
      <div class="prompt-content">
        <p class="prompt-title">댓글을 작성하려면 로그인이 필요해요!</p>
        <p class="prompt-subtitle">다람쥐 친구들과 대화를 나눠보세요 🐿️</p>
        <RouterLink to="/login" class="login-btn">
          <span>🗝️</span>
          로그인하기
        </RouterLink>
      </div>
    </div>

    <!-- 작성 중 애니메이션 -->
    <transition name="bounce">
      <div v-if="isTyping" class="typing-indicator">
        <span class="typing-squirrel">🐿️</span>
        <span class="typing-text">열심히 쓰는 중...</span>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { useUserStore } from '@/stores/user'
import { useCommunityStore } from '@/stores/community'

const props = defineProps({
  articleId: Number,
  mentionText: String
})

const emit = defineEmits(['refresh'])

const userStore = useUserStore()
const communityStore = useCommunityStore()

const newComment = ref('')
const showEmojiPicker = ref(false)
const isTyping = ref(false)
const commentTextarea = ref(null)
const typingTimer = ref(null)

// 이모지 목록
const emojis = ['😊', '😂', '🥰', '😎', '🤔', '👍', '❤️', '🎉', '🙏', '😭', '🔥', '✨']

// 플레이스홀더 텍스트
const placeholders = [
  '따뜻한 댓글을 남겨주세요 🌰',
  '다람쥐들과 이야기를 나눠보세요!',
  '좋은 생각이 있으신가요?',
  '도토리 같은 귀여운 댓글 부탁해요 🐿️'
]

const getPlaceholder = () => {
  const index = Math.floor(Math.random() * placeholders.length)
  return placeholders[index]
}

// mentionText 변경 감지
watch(
  () => props.mentionText,
  (newVal) => {
    if (newVal && !newComment.value.includes(newVal)) {
      newComment.value = `${newVal} ` + newComment.value
      nextTick(() => {
        commentTextarea.value?.focus()
      })
    }
  }
)

// 타이핑 중 표시
watch(newComment, (val) => {
  if (val) {
    isTyping.value = true
    clearTimeout(typingTimer.value)
    typingTimer.value = setTimeout(() => {
      isTyping.value = false
    }, 1000)
  } else {
    isTyping.value = false
  }
})

// 텍스트 영역 높이 자동 조절
const adjustTextareaHeight = (e) => {
  const textarea = e.target
  textarea.style.height = 'auto'
  textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`
}

// 엔터키 처리
const handleEnterKey = (e) => {
  if (!e.shiftKey) {
    submitComment()
  }
}

// 이모지 피커 토글
const toggleEmojiPicker = () => {
  showEmojiPicker.value = !showEmojiPicker.value
}

// 이모지 삽입
const insertEmoji = (emoji) => {
  newComment.value += emoji
  showEmojiPicker.value = false
  commentTextarea.value?.focus()
}

// 도토리 추가
const addAcorn = () => {
  newComment.value += ' 🌰'
  commentTextarea.value?.focus()
}

// 댓글 제출
const submitComment = () => {
  if (!newComment.value.trim() || newComment.value.length > 500) return
  
  communityStore.createComment(props.articleId, newComment.value, () => {
    newComment.value = ''
    showEmojiPicker.value = false
    isTyping.value = false
    emit('refresh')
    
    // 제출 후 애니메이션
    const container = document.querySelector('.comment-form-wrapper')
    container?.classList.add('submit-animation')
    setTimeout(() => {
      container?.classList.remove('submit-animation')
    }, 600)
  })
}
</script>

<style scoped>
.comment-form-container {
  position: relative;
  margin-bottom: 30px;
}

/* 댓글 작성 폼 */
.comment-form-wrapper {
  display: flex;
  gap: 15px;
  padding: 20px;
  background: #f8f8f8;
  border-radius: 20px;
  border: 2px solid #e0e0e0;
  transition: all 0.3s;
}

.comment-form-wrapper:focus-within {
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.user-avatar {
  width: 45px;
  height: 45px;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.avatar-icon {
  font-size: 1.5rem;
}

.comment-input-area {
  flex: 1;
  position: relative;
}

.input-wrapper {
  position: relative;
}

.comment-input {
  width: 100%;
  max-width: 100%;         
  min-width: 0;           
  box-sizing: border-box;  
  padding: 12px 15px;
  border: none;
  background: white;
  border-radius: 15px;
  font-size: 1rem;
  font-family: inherit;
  resize: none;
  transition: all 0.3s;
  line-height: 1.5;
  min-height: 45px;
  max-height: 120px;
  overflow-y: auto;
}

.comment-input:focus {
  outline: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.input-indicator {
  position: absolute;
  bottom: 5px;
  right: 10px;
  font-size: 0.8rem;
  color: #999;
  pointer-events: none;
}

.char-count.warn {
  color: #ff4757;
  font-weight: 600;
}

/* 액션 버튼들 */
.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
  flex-wrap: wrap;
  gap: 10px;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.emoji-btn,
.acorn-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: white;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.emoji-btn:hover,
.acorn-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: #333;
  color: white;
  padding: 5px 10px;
  border-radius: 6px;
  font-size: 0.8rem;
  white-space: nowrap;
  margin-bottom: 5px;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s;
}

.emoji-btn:hover .tooltip,
.acorn-btn:hover .tooltip {
  opacity: 1;
}

/* 제출 버튼 */
.submit-btn {
  padding: 10px 20px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 20px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 6px;
}

.submit-btn:hover:not(:disabled) {
  background: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-icon {
  font-size: 1.1rem;
}

/* 이모지 피커 */
.emoji-picker {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 10px;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 15px;
  padding: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  max-width: 280px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.emoji-item {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s;
}

.emoji-item:hover {
  background: #f0f0f0;
  transform: scale(1.2);
}

/* 로그인 프롬프트 */
.login-prompt {
  background: #f8f8f8;
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  border: 2px dashed #e0e0e0;
}

.prompt-icon {
  margin-bottom: 15px;
}

.sleeping-squirrel {
  font-size: 3rem;
  display: inline-block;
  animation: sleep 3s infinite;
}

@keyframes sleep {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(0.95); }
}

.prompt-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 5px 0;
}

.prompt-subtitle {
  color: #666;
  margin: 0 0 20px 0;
}

.login-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px;
  background: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 20px;
  font-weight: 600;
  transition: all 0.3s;
}

.login-btn:hover {
  background: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

/* 타이핑 인디케이터 */
.typing-indicator {
  position: absolute;
  bottom: -25px;
  left: 65px;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.9rem;
  color: #666;
}

.typing-squirrel {
  animation: bounce 1s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

/* 제출 애니메이션 */
.submit-animation {
  animation: submitPulse 0.6s ease-out;
}

@keyframes submitPulse {
  0% { transform: scale(1); }
  50% { transform: scale(0.98); }
  100% { transform: scale(1); }
}

/* 반응형 */
@media (max-width: 768px) {
  .comment-form-wrapper {
    padding: 15px;
  }

  .user-avatar {
    width: 40px;
    height: 40px;
  }

  .form-actions {
    flex-direction: column;
    gap: 10px;
    align-items: stretch;
  }

  .action-buttons {
    justify-content: center;
  }

  .submit-btn {
    width: 100%;
    justify-content: center;
  }

  .emoji-picker {
    max-width: 240px;
  }
}

/* 다크 모드 */
@media (prefers-color-scheme: dark) {
  .comment-form-wrapper {
    background: #2a2a2a;
    border-color: #444;
  }

  .comment-input {
    background: #333;
    color: #f0f0f0;
  }

  .emoji-btn,
  .acorn-btn {
    background: #333;
  }

  .emoji-picker {
    background: #2a2a2a;
    border-color: #444;
  }

  .emoji-item:hover {
    background: #333;
  }

  .login-prompt {
    background: #2a2a2a;
    border-color: #444;
  }

  .prompt-title {
    color: #f0f0f0;
  }

  .prompt-subtitle {
    color: #b0b0b0;
  }
}

/* 트랜지션 */
.bounce-enter-active,
.bounce-leave-active {
  transition: all 0.3s ease;
}

.bounce-enter-from,
.bounce-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>