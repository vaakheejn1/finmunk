<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, RouterLink, RouterView } from 'vue-router'
import { useUserStore } from '@/stores/user'
import axios from 'axios'
import NotificationList from '@/components/NotificationList.vue' 
import UserProfileModal from '@/components/community/UserProfileModal.vue'


const userStore = useUserStore()
const router = useRouter()

const selectedUserId = ref(null)
const showProfileModal = ref(false)

const openProfileModal = (userId) => {
  selectedUserId.value = userId
  showProfileModal.value = true
}

const logout = () => {
  userStore.logOut()
  router.push('/')
}

const showNotifications = ref(false)
const notifications = ref([])

const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value
}

const loadNotifications = () => {
  if (userStore.token) {
    axios.get(`${import.meta.env.VITE_API_URL}/community/notifications/`, {
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
    .then(res => {
      notifications.value = res.data
    })
    .catch(err => {
      console.error('알림 불러오기 실패:', err)
    })
  }
}

onMounted(() => {
  loadNotifications()
})
</script>

<template>
  <div class="header">
    <div class="header-content">
<RouterLink :to="{ name: 'Home' }" class="logo" style="text-decoration: none;">
  <img 
    src="@/assets/daramlogo1.png" 
    class="logo-img" 
    alt="로고" 
    onerror="this.style.display='none'; this.nextElementSibling.style.display='block';"
  />
  <span class="logo-icon" style="display:none;">🐿️</span>
  <span class="logo-text">FINMUNK</span>
</RouterLink>

      <nav>
        <ul class="nav-menu">
          <li><RouterLink :to="{ name: 'Home' }">홈</RouterLink></li>
          <li><RouterLink :to="{ name: 'Recommend' }">상품추천</RouterLink></li>
          <li><RouterLink :to="{ name: 'Compare' }">상품비교</RouterLink></li>
          <li><RouterLink :to="{ name: 'Market' }">금융정보</RouterLink></li>
          <li><RouterLink :to="{ name: 'Videos' }">주식정보</RouterLink></li>
          <li><RouterLink :to="{ name: 'Community' }">커뮤니티</RouterLink></li>
        </ul>
      </nav>

      <div class="auth-buttons">
        <template v-if="userStore.user">
          <!-- 알림 아이콘 버튼 -->
          <button class="auth-btn notify-btn" @click="toggleNotifications">🔔</button>
          <NotificationList
            v-if="showNotifications"
            :notifications="notifications"
            @close="showNotifications = false"
            @show-profile="openProfileModal"
          />

          <button class="auth-btn mypage-btn">
            <RouterLink :to="{ name: 'MyPage' }">마이페이지</RouterLink>
          </button>
          <button class="auth-btn login-btn" @click="logout">로그아웃</button>
        </template>
        <template v-else>
          <button class="auth-btn login-btn">
            <RouterLink :to="{ name: 'Login' }">로그인</RouterLink>
          </button>
          <button class="auth-btn signup-btn">
            <RouterLink :to="{ name: 'Signup' }">회원가입</RouterLink>
          </button>


          
        </template>
      </div>
    </div>
  </div>

  <div class="page-content">
    <RouterView />
  </div>
<footer class="main-footer">
  <div class="container">
    <div class="footer-content">
      <div class="footer-logo">
        <span class="logo-text">FINMUNK</span>
        <span class="logo-subtitle">혁신적인 금융 플랫폼</span>
      </div>
      <div class="footer-copy">
        ⓒ 2025 FINMUNK. All rights reserved.
      </div>
    </div>
  </div>
</footer>

<UserProfileModal
  v-if="showProfileModal && selectedUserId"
  :userId="selectedUserId"
  :show="true"
  @close="showProfileModal = false"
/>


</template>

<style scoped>
.header {
  background-color: #fff;
  border-bottom: 1px solid #f0f0f0;
  position: fixed;
  width: 100%;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.page-content {
  padding-top: 80px;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 24px;
  font-weight: bold;
}

.logo-img {
  height: 36px;
  width: auto;
}

.logo-icon {
  font-size: 32px;
}

.logo-text {
  color: #4DD0B1;
  font-weight: 800;
  letter-spacing: -0.5px;
}

.nav-menu {
  display: flex;
  gap: 36px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-menu a {
  text-decoration: none;
  color: #666;
  font-weight: 500;
  font-size: 15px;
  transition: color 0.2s;
}

.nav-menu a:hover,
.nav-menu a.router-link-active,
.nav-menu a.router-link-exact-active {
  color: #4DD0B1;
}

.auth-buttons {
  display: flex;
  gap: 12px;
}

.auth-btn {
  padding: 8px 20px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 500;
  font-size: 14px;
  transition: all 0.2s;
}

.auth-btn a {
  text-decoration: none;
  color: inherit;
}

.login-btn,
.signup-btn {
  background-color: #fff;
  color: #666;
  border: 1px solid #e0e0e0;
}

.login-btn:hover,
.signup-btn:hover {
  background-color: #f8f8f8;
  border-color: #d0d0d0;
}

.mypage-btn {
  background-color: #4DD0B1;
  color: white;
}

.mypage-btn:hover {
  background-color: #3CBFA0;
}

.notify-btn {
  background-color: #fff;
  color: #666;
  border: 1px solid #e0e0e0;
  font-size: 18px;
  padding: 6px 12px;
}

.notify-btn:hover {
  background-color: #f0f0f0;
}


/* footer */
/* 푸터 */
.main-footer {
  background: linear-gradient(135deg, rgb(255, 255, 255) 0%, white 100%);
  color: white;
  padding: 3rem 0;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
}

.footer-logo {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding-left: 1rem;
  padding-right: 1rem;
}

.logo-text {
  font-size: 2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.logo-subtitle {
  font-size: 0.9rem;
  color: #9ca3af;
}

.footer-copy {
  color: #9ca3af;
  font-size: 0.9rem;
}

</style>
