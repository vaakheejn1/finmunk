<template>
  <div v-if="show" class="modal-backdrop" @click.self="closeModal">
    <div class="modal-box">
      <header class="modal-header">
        <h3 v-if="userInfo">🐿️ @{{ userInfo.username }} 프로필</h3>
        <button @click="closeModal" class="close-btn">✖️</button>
      </header>

      <div v-if="userInfo" class="profile-content">
        <div class="user-basic-info">
          <p v-if="userInfo.bio" class="user-bio">"{{ userInfo.bio }}"</p>
          <p>🎂 나이: {{ userInfo.age }}세 / 💼 직업: {{ userInfo.job ? '있음' : '없음' }}</p>
          <p>💰 수입: {{ userInfo.income }} / 🏠 자산: {{ userInfo.assets }}</p>
        </div>

        <div class="follow-section">
          <p>🌰 팔로워: {{ userInfo.followers_count }}명 / 🐿️ 팔로잉: {{ userInfo.followings_count }}명</p>

          <button
            v-if="userInfo.id !== userStore.user.id"
            @click="toggleFollow"
            class="follow-btn"
            :class="{ 'following': userInfo.is_following }"
          >
            {{ userInfo.is_following ? '🙈 언팔로우' : '🤝 팔로우' }}
          </button>
        </div>

        <hr class="divider" />
      </div>

      <div v-else class="loading-state">
        <div class="loading-squirrel">🐿️</div>
        <p>다람쥐가 도토리를 모으고 있어요...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user'

const props = defineProps({
  userId: Number,
  show: Boolean
})
const emit = defineEmits(['close'])

const userStore = useUserStore()
const userInfo = ref(null)
const userArticles = ref([])
const userComments = ref([])

const closeModal = () => {
  emit('close')
}

const authHeaders = {
  headers: { Authorization: `Token ${userStore.token}` }
}

const fetchUserProfile = () => {
  axios.get(`${import.meta.env.VITE_API_URL}/users/profile/${props.userId}/`, authHeaders)
    .then(res => {
      userInfo.value = res.data
    })
    .catch(err => {
      console.error('유저 프로필 오류:', err)
    })
}

const fetchUserArticles = () => {
  axios.get(`${import.meta.env.VITE_API_URL}/community/articles/?user=${props.userId}`, authHeaders)
    .then(res => {
      userArticles.value = res.data
    })
    .catch(err => {
      console.error('유저 글 오류:', err)
    })
}

const fetchUserComments = () => {
  axios.get(`${import.meta.env.VITE_API_URL}/community/comments/?user=${props.userId}`, authHeaders)
    .then(res => {
      userComments.value = res.data
    })
    .catch(err => {
      console.error('유저 댓글 오류:', err)
    })
}

const toggleFollow = () => {
  axios.post(`${import.meta.env.VITE_API_URL}/users/follow/${props.userId}/`, {}, authHeaders)
    .then(res => {
      // 상태만 수정하는 대신 전체 정보 다시 받아오기
      fetchUserProfile()
    })
    .catch(err => {
      console.error('팔로우 오류:', err)
    })
}


watch(() => props.userId, () => {
  if (props.userId) {
    fetchUserProfile()
    fetchUserArticles()
    fetchUserComments()
  }
})

onMounted(() => {
  if (props.userId) {
    fetchUserProfile()
    fetchUserArticles()
    fetchUserComments()
  }
})
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  background: rgba(255, 255, 255, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  backdrop-filter: blur(3px);
  padding: 20px;
  box-sizing: border-box;
}

.modal-box {
  background: linear-gradient(135deg, #FFF8DC, #F5DEB3);
  border: 3px solid #D2691E;
  border-radius: 20px;
  padding: 25px;
  width: 100%;
  max-width: 550px;
  max-height: calc(100vh - 40px);
  overflow-y: auto;
  box-shadow: 0 8px 32px rgba(139, 69, 19, 0.3);
  position: relative;
  margin: auto;
}


.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px dashed #D2691E;
}

.modal-header h3 {
  color: #8B4513;
  font-weight: bold;
  font-size: 20px;
  margin: 0;
}

.close-btn {
  background: #CD853F;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.close-btn:hover {
  background: #A0522D;
  transform: scale(1.1);
}

.profile-content {
  color: #8B4513;
}

.user-basic-info {
  background: rgba(255, 255, 255, 0.6);
  padding: 15px;
  border-radius: 15px;
  margin-bottom: 15px;
  border: 2px solid #DEB887;
  word-break: keep-all; 
  line-height: 1.6;
  text-align: center;
}

.user-basic-info p {
  margin: 8px 0;
  font-weight: 500;
  display: flex;
  justify-content: center;
  gap: 6px;
  flex-wrap: wrap;
}

.follow-section {
  text-align: center;
  margin: 20px 0;
}

.follow-section p {
  font-weight: 600;
  color: #A0522D;
  margin-bottom: 15px;
}

.follow-btn {
  background: linear-gradient(45deg, #32CD32, #228B22);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  cursor: pointer;
  font-weight: bold;
  font-size: 16px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(50, 205, 50, 0.3);
}

.follow-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(50, 205, 50, 0.4);
}

.follow-btn.following {
  background: linear-gradient(45deg, #FF6347, #DC143C);
  box-shadow: 0 4px 15px rgba(255, 99, 71, 0.3);
}

.follow-btn.following:hover {
  box-shadow: 0 6px 20px rgba(255, 99, 71, 0.4);
}

.divider {
  border: none;
  height: 2px;
  background: linear-gradient(90deg, transparent, #D2691E, transparent);
  margin: 25px 0;
}

.content-section {
  margin-bottom: 25px;
}

.content-section h4 {
  color: #A0522D;
  font-size: 18px;
  margin-bottom: 15px;
  padding: 10px;
  background: rgba(210, 105, 30, 0.1);
  border-radius: 10px;
  border-left: 4px solid #D2691E;
}

.content-list {
  max-height: 200px;
  overflow-y: auto;
  padding: 5px;
}

.article-item, .comment-item {
  margin-bottom: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 10px;
  border-left: 3px solid #DEB887;
  transition: all 0.3s ease;
}

.article-item:hover, .comment-item:hover {
  transform: translateX(5px);
  background: rgba(255, 255, 255, 0.9);
  border-left-color: #D2691E;
}

.content-link {
  color: #8B4513;
  text-decoration: none;
  font-weight: 500;
  display: block;
  transition: color 0.3s ease;
}

.content-link:hover {
  color: #A0522D;
  text-decoration: underline;
}

.empty-state {
  text-align: center;
  padding: 30px;
  color: #A0522D;
  font-style: italic;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 15px;
  border: 2px dashed #DEB887;
}

.loading-state {
  text-align: center;
  padding: 50px;
  color: #A0522D;
}

.loading-squirrel {
  font-size: 48px;
  animation: bounce 1s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

/* 스크롤바 스타일링 */
.content-list::-webkit-scrollbar,
.modal-box::-webkit-scrollbar {
  width: 8px;
}

.content-list::-webkit-scrollbar-track,
.modal-box::-webkit-scrollbar-track {
  background: rgba(222, 184, 135, 0.3);
  border-radius: 10px;
}

.content-list::-webkit-scrollbar-thumb,
.modal-box::-webkit-scrollbar-thumb {
  background: #D2691E;
  border-radius: 10px;
}

.content-list::-webkit-scrollbar-thumb:hover,
.modal-box::-webkit-scrollbar-thumb:hover {
  background: #A0522D;
}

/* 모바일 대응 */
@media (max-width: 768px) {
  .modal-backdrop {
    padding: 10px;
  }
  
  .modal-box {
    max-width: 100%;
    max-height: calc(100vh - 20px);
    padding: 20px;
  }
  
  .modal-header h3 {
    font-size: 18px;
  }
  
  .follow-btn {
    padding: 10px 20px;
    font-size: 14px;
  }
}
</style>