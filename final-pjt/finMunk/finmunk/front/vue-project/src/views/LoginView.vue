<template>
  <div class="login-container">
    <div class="login-card">
      <h2 class="login-title">🐿️ 환영합니다!</h2>
      <p class="login-subtitle">도토리 지갑을 열어볼까요?</p>
      <form @submit.prevent="login" class="login-form">
        <input 
          v-model="username" 
          type="text" 
          placeholder="유저네임" 
          class="login-input"
          :disabled="isLoading"
        />
        <input 
          v-model="password" 
          type="password" 
          placeholder="비밀번호" 
          class="login-input"
          :disabled="isLoading"
        />
        <button 
          class="login-btn" 
          :disabled="isLoading"
          :class="{ 'loading': isLoading }"
        >
          {{ isLoading ? '로그인 중...' : '로그인' }}
        </button>
      </form>
      <p class="login-footer">
        아직 회원이 아니신가요?
        <RouterLink :to="{ name: 'Signup' }" class="signup-link">회원가입</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'

const username = ref('')
const password = ref('')
const store = useUserStore()
const isLoading = ref(false) // 로딩 상태 추가

const login = async () => {
  // 입력 값 검증
  if (!username.value.trim()) {
    alert('❌ 아이디를 입력해주세요.')
    return
  }
  
  if (!password.value.trim()) {
    alert('❌ 비밀번호를 입력해주세요.')
    return
  }

  try {
    isLoading.value = true
    await store.logIn({ 
      username: username.value.trim(), 
      password: password.value 
    })
    // 성공 시 store에서 자동으로 라우팅됨
  } catch (error) {
    // store에서 이미 alert를 처리했으므로 추가 처리는 필요 없음
    console.error('로그인 실패:', error)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: calc(100vh - 120px);
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f8fdf8;
  padding: 40px 20px;
}

.login-card {
  background: white;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  width: 100%;
  text-align: center;
  animation: slideFadeIn 0.5s ease-out;
}

@keyframes slideFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-title {
  font-size: 2rem;
  margin-bottom: 10px;
  color: #2c3e50;
}

.login-subtitle {
  font-size: 1rem;
  color: #6b7280;
  margin-bottom: 30px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.login-input {
  padding: 12px 16px;
  font-size: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 15px;
  background: #f9f9f9;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.login-input:focus {
  outline: none;
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
  background: white;
}

.login-btn {
  padding: 12px 16px;
  font-size: 1rem;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  border: none;
  border-radius: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
}

.login-footer {
  margin-top: 24px;
  font-size: 0.95rem;
  color: #6b7280;
}

.signup-link {
  margin-left: 5px;
  color: #10b981;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.2s;
}

.signup-link:hover {
  color: #059669;
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.login-btn.loading {
  background: linear-gradient(135deg, #6b7280 0%, #9ca3af 100%);
}

</style>
