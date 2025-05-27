<template>
  <div class="chatbot-container">
    <!-- 채팅 토글 버튼 -->
    <div class="chat-toggle" @click="toggleChat" :class="{ active: isOpen }">
      <div class="toggle-icon-wrapper">
        <img v-if="!isOpen" :src="daramchat" alt="람쥐 아이콘" class="chat-toggle-img" />
        <div v-else class="close-icon">✕</div>
      </div>
      <div class="ripple-effect" v-if="!isOpen"></div>
      <!-- 알림 배지 -->
      <div v-if="unreadCount > 0 && !isOpen" class="notification-badge">{{ unreadCount }}</div>
    </div>

    <!-- 채팅 창 -->
    <Transition name="chat-window" appear>
      <div v-if="isOpen" class="chat-window">
        <!-- 헤더 -->
        <div class="chat-header">
          <div class="header-content">
            <div class="bot-avatar">
              <img :src="daramchat" alt="람쥐" class="avatar-img" />
              <div class="online-indicator"></div>
            </div>
            <div class="header-info">
              <h3 class="bot-name">람쥐봇</h3>
              <p class="bot-status">온라인 🐿️</p>
            </div>
          </div>
        </div>

        <!-- 채팅 본문 -->
        <div class="chat-body" ref="chatBody">
          <TransitionGroup name="message" tag="div">
            <div 
              v-for="msg in messages" 
              :key="msg.id" 
              :class="['chat-message', msg.role]"
            >
              <div v-if="msg.role === 'user'" class="message-wrapper user-message">
                <div class="message-content">
                  <span class="message-text">{{ msg.content }}</span>
                </div>
                <div class="user-avatar">👤</div>
              </div>
              
              <div v-else class="message-wrapper bot-message">
                <div class="bot-message-avatar">
                  <img :src="daramchat" alt="람쥐" class="mini-avatar" />
                </div>
                <div class="message-content">
                  <span class="message-text" v-html="convertLinks(msg.content)"></span>
                  <div class="message-time">{{ formatTime(msg.timestamp) }}</div>
                </div>
              </div>
            </div>
          </TransitionGroup>
          
          <!-- 타이핑 인디케이터 -->
          <div v-if="isTyping" class="typing-indicator">
            <div class="typing-avatar">
              <img :src="daramchat" alt="람쥐" class="mini-avatar" />
            </div>
            <div class="typing-content">
              <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>

        <!-- 입력 영역 -->
        <div class="chat-input-area">
          <div class="input-wrapper">
            <input
              v-model="input"
              @keyup.enter="sendMessage"
              @focus="onInputFocus"
              @blur="onInputBlur"
              placeholder="질문을 입력해보세요..."
              :disabled="isTyping"
              class="chat-input"
            />
            <button 
              @click="sendMessage" 
              :disabled="!input.trim() || isTyping"
              class="send-button"
              :class="{ active: input.trim() }"
            >
              <div class="send-icon">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22 2L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
            </button>
          </div>
          
          <!-- 빠른 응답 버튼들 -->
          <div class="quick-actions" v-if="!hasUserMessage">
            <button @click="sendQuickMessage('상품 추천받고 싶어요')" class="quick-button">
              💡 상품 추천
            </button>
            <button @click="sendQuickMessage('금리 비교하고 싶어요')" class="quick-button">
              📊 금리 비교
            </button>
            <button @click="sendQuickMessage('주변 은행 찾아주세요')" class="quick-button">
              🏦 은행 찾기
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, nextTick, computed } from 'vue'
import axios from 'axios'
import daramchat from '@/assets/daramchat.png'
const siteUrl = import.meta.env.VITE_SITE_URL


const isOpen = ref(false)
const input = ref('')
const chatBody = ref(null)
const isTyping = ref(false)
const unreadCount = ref(0)
const API_URL = import.meta.env.VITE_API_URL

const messages = ref([
  { 
    id: 0, 
    role: 'bot', 
    content: '안녕하세요! 람쥐입니다 🐿️\n무엇을 도와드릴까요?',
    timestamp: new Date()
  }
])

const hasUserMessage = computed(() => {
  return messages.value.some(msg => msg.role === 'user')
})

function toggleChat() {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    unreadCount.value = 0
    scrollToBottom()
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (chatBody.value) {
      chatBody.value.scrollTop = chatBody.value.scrollHeight
    }
  })
}

function formatTime(timestamp) {
  return timestamp ? timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : ''
}

function onInputFocus() {
  setTimeout(scrollToBottom, 100)
}

function onInputBlur() {
  // 입력 포커스 해제 시 처리
}

function convertLinks(text) {
  return text
    .replace(/(예\/적금 추천 바로가기)/g, `<a href="${siteUrl}/recommend" target="_blank" class="chat-link">$1</a>`)
    .replace(/(예\/적금 비교 바로가기)/g, `<a href="${siteUrl}/compare" target="_blank" class="chat-link">$1</a>`)
    .replace(/(금융정보 바로가기)/g, `<a href="${siteUrl}/market" target="_blank" class="chat-link">$1</a>`)
    .replace(/(홈화면 바로가기)/g, `<a href="${siteUrl}" target="_blank" class="chat-link">$1</a>`)
    .replace(/(주식정보 바로가기)/g, `<a href="${siteUrl}/videos" target="_blank" class="chat-link">$1</a>`)
    .replace(/(주변 은행 바로가기)/g, `<a href="${siteUrl}/bankmap" target="_blank" class="chat-link">$1</a>`)
}

function sendQuickMessage(message) {
  input.value = message
  sendMessage()
}

function sendMessage() {
  if (!input.value.trim() || isTyping.value) return

  const userMessage = { 
    id: Date.now(), 
    role: 'user', 
    content: input.value,
    timestamp: new Date()
  }
  messages.value.push(userMessage)
  
  const messageToSend = input.value
  input.value = ''
  
  isTyping.value = true
  scrollToBottom()

  // 타이핑 시뮬레이션
  setTimeout(() => {
    axios.post(`${API_URL}/chatbot/chat/`, { message: messageToSend })
      .then(res => {
        isTyping.value = false
        messages.value.push({ 
          id: Date.now() + 1, 
          role: 'bot', 
          content: res.data.reply,
          timestamp: new Date()
        })
        if (!isOpen.value) {
          unreadCount.value++
        }
        scrollToBottom()
      })
      .catch(err => {
        isTyping.value = false
        messages.value.push({ 
          id: Date.now() + 1, 
          role: 'bot', 
          content: 'GPT와 연결할 수 없습니다 ㅠㅠ\n' + (err.response?.data?.error || err.message),
          timestamp: new Date()
        })
        if (!isOpen.value) {
          unreadCount.value++
        }
        scrollToBottom()
      })
  }, 1000 + Math.random() * 1000) // 1-2초 랜덤 지연
}


function openChatbot() {
  if (!isOpen.value) {
    toggleChat()
  }
}

defineExpose({
  openChatbot
})


</script>

<style scoped>
.chatbot-container {
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: 1500;
}

/* 토글 버튼 */
.chat-toggle {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 8px 32px rgba(16, 185, 129, 0.4);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.chat-toggle:hover {
  transform: translateY(-4px) scale(1.05);
  box-shadow: 0 12px 40px rgba(16, 185, 129, 0.5);
}

.chat-toggle.active {
  background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
  box-shadow: 0 8px 32px rgba(239, 68, 68, 0.4);
}

.toggle-icon-wrapper {
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-toggle-img {
  width: 45px;
  height: 45px;
  object-fit: contain;
  filter: brightness(0) invert(1);
  transition: all 0.3s ease;
}

.close-icon {
  font-size: 24px;
  color: white;
  font-weight: 600;
}

.ripple-effect {
  display: none;
}

@keyframes ripple {
  0% {
    transform: translate(-50%, -50%) scale(0);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -50%) scale(2);
    opacity: 0;
  }
}

.notification-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
  color: white;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  animation: bounce 1s infinite;
}

/* 채팅 창 */
.chat-window {
  position: absolute;
  bottom: 90px;
  right: 0;
  width: 380px;
  max-height: 600px;
  background: linear-gradient(135deg, #ffffff 0%, #f8fffe 100%);
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* 채팅 창 애니메이션 */
.chat-window-enter-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.chat-window-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.chat-window-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.9);
}

.chat-window-leave-to {
  opacity: 0;
  transform: translateY(10px) scale(0.95);
}

/* 헤더 */
.chat-header {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  color: white;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.chat-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="10" cy="10" r="1" fill="rgba(255,255,255,0.1)"><animate attributeName="opacity" dur="3s" repeatCount="indefinite" values="0.1;0.3;0.1"/></circle><circle cx="90" cy="20" r="1" fill="rgba(255,255,255,0.1)"><animate attributeName="opacity" dur="4s" repeatCount="indefinite" values="0.1;0.4;0.1"/></circle></svg>');
}

.header-content {
  display: flex;
  align-items: center;
  position: relative;
  z-index: 1;
}

.bot-avatar {
  position: relative;
  margin-right: 12px;
}

.avatar-img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  padding: 6px;
}

.online-indicator {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 12px;
  height: 12px;
  background: #22c55e;
  border-radius: 50%;
  border: 2px solid white;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.header-info {
  flex: 1;
}

.bot-name {
  font-size: 16px;
  font-weight: 700;
  margin: 0 0 2px 0;
}

.bot-status {
  font-size: 12px;
  margin: 0;
  opacity: 0.9;
}

/* 채팅 본문 */
.chat-body {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  max-height: 400px;
  scroll-behavior: smooth;
}

.chat-body::-webkit-scrollbar {
  width: 6px;
}

.chat-body::-webkit-scrollbar-track {
  background: transparent;
}

.chat-body::-webkit-scrollbar-thumb {
  background: rgba(16, 185, 129, 0.3);
  border-radius: 3px;
}

.chat-body::-webkit-scrollbar-thumb:hover {
  background: rgba(16, 185, 129, 0.5);
}

/* 메시지 애니메이션 */
.message-enter-active {
  transition: all 0.4s ease;
}

.message-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.chat-message {
  margin-bottom: 16px;
}

.message-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  animation: messageSlideIn 0.4s ease-out;
}

@keyframes messageSlideIn {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.user-message {
  justify-content: flex-end;
}

.bot-message {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
  position: relative;
}

.user-message .message-content {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
  padding: 12px 16px;
  border-radius: 18px 18px 4px 18px;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.bot-message .message-content {
  background: linear-gradient(135deg, #f1f5f9 0%, #ffffff 100%);
  color: #374151;
  padding: 12px 16px;
  border-radius: 18px 18px 18px 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.message-text {
  font-size: 14px;
  line-height: 1.5;
  word-wrap: break-word;
}

.message-time {
  font-size: 10px;
  color: #9ca3af;
  margin-top: 4px;
  text-align: right;
}

.user-avatar {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #6b7280 0%, #9ca3af 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.bot-message-avatar {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
}

.mini-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(16, 185, 129, 0.1);
  padding: 4px;
}

/* 타이핑 인디케이터 */
.typing-indicator {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  margin-bottom: 16px;
  animation: fadeIn 0.3s ease;
}

.typing-avatar {
  width: 32px;
  height: 32px;
}

.typing-content {
  background: linear-gradient(135deg, #f1f5f9 0%, #ffffff 100%);
  padding: 12px 16px;
  border-radius: 18px 18px 18px 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.typing-dots {
  display: flex;
  gap: 4px;
}

.typing-dots span {
  width: 6px;
  height: 6px;
  background: #10b981;
  border-radius: 50%;
  animation: typingDot 1.4s infinite;
}

.typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typingDot {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.4;
  }
  30% {
    transform: translateY(-8px);
    opacity: 1;
  }
}

/* 입력 영역 */
.chat-input-area {
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  padding: 16px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
}

.input-wrapper {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.chat-input {
  flex: 1;
  border: 2px solid rgba(16, 185, 129, 0.1);
  background: white;
  padding: 12px 16px;
  border-radius: 25px;
  font-size: 14px;
  transition: all 0.3s ease;
  outline: none;
}

.chat-input:focus {
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.send-button {
  width: 45px;
  height: 45px;
  background: linear-gradient(135deg, #e5e7eb 0%, #f3f4f6 100%);
  color: #9ca3af;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.send-button.active {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  color: white;
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.send-button:hover:not(:disabled) {
  transform: translateY(-2px);
}

.send-icon {
  width: 20px;
  height: 20px;
}

/* 빠른 응답 버튼들 */
.quick-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.quick-button {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  color: #166534;
  border: 1px solid rgba(22, 101, 52, 0.2);
  padding: 8px 12px;
  border-radius: 20px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.quick-button:hover {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3);
}

/* 링크 스타일 */
:deep(.chat-link) {
  color: #10b981;
  text-decoration: none;
  font-weight: 600;
  padding: 2px 6px;
  background: rgba(16, 185, 129, 0.1);
  border-radius: 4px;
  transition: all 0.2s ease;
}

:deep(.chat-link:hover) {
  background: rgba(16, 185, 129, 0.2);
  transform: translateY(-1px);
}

/* 반응형 */
@media (max-width: 768px) {
  .chat-window {
    width: 340px;
    bottom: 85px;
    right: -10px;
  }
  
  .chatbot-container {
    bottom: 20px;
    right: 20px;
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-3px);
  }
  60% {
    transform: translateY(-1px);
  }
}
</style>