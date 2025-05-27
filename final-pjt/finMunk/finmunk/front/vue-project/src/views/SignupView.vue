<template>
  <div class="signup-container">
    <div class="form-box">
      <h2 class="form-title">회원가입</h2>
      <form @submit.prevent="onSignUp" class="signup-form">
        <input v-model="username" type="text" placeholder="사용자명 (username)" required />
        <input v-model="email" type="email" placeholder="이메일 (email)" required />
        <input v-model="age" type="number" placeholder="나이 (선택)" />
        <select v-model="job" required>
          <option value="">직업 유무</option>
          <option value="true">직업 있음</option>
          <option value="false">직업 없음</option>
        </select>
        <input v-model="income" type="number" placeholder="월 소득 (만원)" />
        <input v-model="assets" type="number" placeholder="총 자산 (만원)" />
        <input v-model="password1" type="password" placeholder="비밀번호" required />
        <input v-model="password2" type="password" placeholder="비밀번호 확인" required />

        <button type="submit" class="submit-btn">회원가입</button>
      </form>

      <p class="form-footer">
        이미 계정이 있으신가요?
        <RouterLink :to="{ name: 'Login' }" class="link">로그인</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const username = ref('')
const email = ref('')
const age = ref('')
const job = ref('')
const income = ref('')
const assets = ref('')
const password1 = ref('')
const password2 = ref('')

const onSignUp = () => {
  if (password1.value !== password2.value) {
    alert('❌ 비밀번호가 일치하지 않아요!')
    return
  }

  const userInfo = {
    username: username.value,
    email: email.value,
    age: age.value ? Number(age.value) : null,
    job: job.value === 'true',
    income: income.value ? Number(income.value) : null,
    assets: assets.value ? Number(assets.value) : null,
    password1: password1.value,
    password2: password2.value,
  }

  userStore.signUp(userInfo)
    .catch(err => {
      if (err.response && err.response.data) {
        const errorData = err.response.data
        if (errorData.password1 && errorData.password1[0].includes('too short')) {
          alert('❗ 비밀번호는 최소 8자 이상이어야 해요!')
        } else {
          const messages = Object.values(errorData).flat().join('\n')
          alert('회원가입 실패:\n' + messages)
        }
      } else {
        alert('알 수 없는 오류가 발생했어요 🐿️')
      }
    })
}
</script>

<style scoped>
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 100px 20px 40px;
  background: #f8fdf8;
  min-height: 100vh;
}

.form-box {
  background: white;
  padding: 40px;
  border-radius: 20px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.5s ease;
}

.form-title {
  text-align: center;
  margin-bottom: 30px;
  color: #10b981;
  font-size: 1.8rem;
  font-weight: bold;
}

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.signup-form input,
.signup-form select {
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  transition: all 0.3s;
}

.signup-form input:focus,
.signup-form select:focus {
  outline: none;
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
}

.submit-btn {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  color: white;
  font-weight: bold;
  padding: 12px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(16, 185, 129, 0.3);
}

.form-footer {
  text-align: center;
  margin-top: 20px;
  color: #555;
  font-size: 0.95rem;
}

.link {
  color: #10b981;
  font-weight: bold;
  margin-left: 6px;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
